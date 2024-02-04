#pragma once

#include<iostream>
#include <cstdint>
#include <climits>
#include <cassert>
#include <string>

using std::string;

namespace redtime
{
	class time
	{
	public:
		time(int year = 0, int month = 0, int day = 0, int hour = 0, int minute = 0, int second = 0, int msecond = 0) : _values{ year, month, day, hour, minute, second, msecond } {};
		time(const time&) = default;

		int64_t year() const
		{
			return _values[0];
		};
		int64_t month() const
		{
			return _values[1];
		};
		int64_t day() const
		{
			return _values[2];
		};
		int64_t hour() const
		{
			return _values[3];
		};
		int64_t minute() const
		{
			return _values[4];
		};
		int64_t second() const
		{
			return _values[5];
		};
		int64_t msecond() const
		{
			return _values[6];
		};
		virtual void year(int64_t val) = 0;
		virtual void month(int64_t val) = 0;
		virtual void day(int64_t val) = 0;
		virtual void hour(int64_t val) = 0;
		virtual void minute(int64_t val) = 0;
		virtual void second(int64_t val) = 0;
		virtual void msecond(int64_t val) = 0;

		virtual string str() = 0;

		void sim_dhms();
		int64_t seconds() const;
		int64_t months() const;

	protected:
		int64_t _values[7];
	};

	class itvtime : public time
	{
	public:
		friend class realtime;
		using time::year;
		using time::month;
		using time::day;
		using time::hour;
		using time::minute;
		using time::second;
		using time::msecond;
		itvtime(int year = 0, int month = 0, int day = 0, int hour = 0, int minute = 0, int second = 0, int msecond = 0) : time(year, month, day, hour, minute, second, msecond) {};
		itvtime(const itvtime& t2) = default;

		void year(const int64_t val)
		{
			_values[0] = val;
		};
		void month(const int64_t val)
		{
			_values[1] = val;
		};
		void day(const int64_t val)
		{
			_values[2] = val;
		};
		void hour(const int64_t val)
		{
			_values[3] = val;
		};
		void minute(const int64_t val)
		{
			_values[4] = val;
		};
		void second(const int64_t val)
		{
			_values[5] = val;
		};
		void msecond(const int64_t val)
		{
			_values[6] = val;
		};

		itvtime operator+(const itvtime& t2) const;
		itvtime& operator+=(const itvtime& t2);
		itvtime operator-(const itvtime& t2) const;
		itvtime& operator-=(const itvtime& t2);

		itvtime& add(const itvtime& t2);
		itvtime& add(const itvtime* pt2);
		itvtime& sub(const itvtime& t2);
		itvtime& sub(const itvtime* pt2);

		void sim();

		string str();

	};

	enum class realevel
	{
		UNKNOWN = -1,
		YEAR = 0,
		MONTH = 1,
		DAY = 2,
		HOUR = 3,
		MINUTE = 4,
		SECOND = 5,
		MSECOND = 6
	};

	class realtime : time
	{
	public:
		using time::year;
		using time::month;
		using time::day;
		using time::hour;
		using time::minute;
		using time::second;
		using time::msecond;
		realtime(int year, int month = -1, int day = -1, int hour = -1, int minute = -1, int second = -1, int msecond = -1) : time(year, month, day, hour, minute, second, msecond) {
			check();
		}

		realevel get_level()
		{
			if (rlevel != realevel::UNKNOWN)
				return rlevel;
			for (int i = 0; i < 7; i++) {
				if (_values[i] < 0) {
					rlevel = static_cast<realevel>(i - 1);  //@sk exp since the values for realevel::* are manuall orgnized
					break;
				}
			}
			return rlevel;
		};

		//realevel get_level() const
		//{
		//	if (rlevel != realevel::UNKNOWN)
		//		return rlevel;
		//	else
		//		throw(std::runtime_error(""));
		//};

		void year(const int64_t val)
		{
			_values[0] = val;
		};
		void month(const int64_t val)
		{
			_values[1] = val;
		};
		void day(const int64_t val)
		{
			_values[2] = val;
		};
		void hour(const int64_t val)
		{
			_values[3] = val;
		};
		void minute(const int64_t val)
		{
			_values[4] = val;
		};
		void second(const int64_t val)
		{
			_values[5] = val;
		};
		void msecond(const int64_t val)
		{
			_values[6] = val;
		};

		realtime& operator+=(const itvtime& itv);
		realtime operator+(const itvtime& itv) const;

		realtime& operator-=(const itvtime& itv);
		realtime operator-(const itvtime& itv) const;
		itvtime operator-(const realtime& itv) const;



		static int get_days_from_ym(int year, int month);
		static bool isLeap(int year);

		string str();
		void sim();
		int64_t stamp() const;


		static int64_t countLeap(long year1, long year2, bool leftOC = true, bool rightOC = true);
		static int get_jdays(int month, int day, int year = 1);
	private:
		realevel rlevel = realevel::UNKNOWN;
		void check() {
			//std::cout << static_cast<int>(get_level()) << std::endl;
			//std::cout << "what?????" << std::endl;
			if (get_level() >= realevel::MONTH && month() <= 0 || month() >= 13)
				throw(std::runtime_error(""));
			if (get_level() >= realevel::DAY && (day() <= 0 || day() > realtime::get_days_from_ym(year(), month())))
				throw(std::runtime_error(""));
			if (get_level() >= realevel::HOUR && (hour() < 0 || hour() >= 24))
				throw(std::runtime_error(""));
			if (get_level() >= realevel::MINUTE && (minute() < 0 || minute() >= 60))
				throw(std::runtime_error(""));
			if (get_level() >= realevel::SECOND && (second() < 0 || second() >= 60))
					throw(std::runtime_error(""));
			if (get_level() >= realevel::MSECOND && (msecond() < 0 || msecond() >= 1000))
				throw(std::runtime_error(""));
		}
	};

	class abstime : time
	{
	};
};

// class redtime
// {
// public:
//     long year;
//     long month;
//     long day;
//     long hour;
//     long minute;
//     long second;
//     redtime(int year = 0, int month = 0, int day = 0, int hour = 0, int minute = 0, int second = 0) : year(year), month(month), day(day), hour(hour), minute(minute), second(second){};

//     redtime operator+(const redtime &t2);
//     redtime &operator+=(const redtime &t2);
//     redtime operator-(const redtime &t2) const;
//     redtime &operator-=(const redtime &t2);

//     redtime *add(const redtime &t2);
//     redtime *add(const redtime *pt2);

//     redtime *sub(const redtime &t2);
//     redtime *sub(const redtime *pt2);
//     // redtime operator*(const redtime &t2);
//     redtime &sim();
//     long stamp() const;
//     redtime &real();
//     redtime &reset();

//     static int get_days_from_ym(int year, int month);
//     static bool isLeap(int year);

//     redtime &lastMonth();
//     redtime &nextMonth();

//     static redtime *realtime(int year = 0, int month = 0, int day = 0, int hour = 0, int minute = 0, int second = 0);
//     static redtime *abstime(int year = 0, int month = 0, int day = 0, int hour = 0, int minute = 0, int second = 0);

//     static redtime getDuration(const redtime &rt1, const redtime &rt2);
//     static void lastMonth(long &year, long &month);
//     static void nextMonth(long &year, long &month);


// private:
//     bool isreal = false;
// };
