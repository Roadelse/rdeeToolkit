#pragma once

#include <iostream>
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
		time(int year = 0, int month = 0, int day = 0, int hour = 0, int minute = 0, int second = 0, int msecond = 0) : _values{year, month, day, hour, minute, second, msecond} {};
		time(const time &frt) : _values{frt._values[0], frt._values[1], frt._values[2], frt._values[3], frt._values[4], frt._values[5], frt._values[6]} {};
		time(time &&) = default;

		int64_t year() const { return _year; };
		int64_t month() const { return _month; };
		int64_t day() const { return _day; };
		int64_t hour() const { return _hour; };
		int64_t minute() const { return _minute; };
		int64_t second() const { return _second; };
		int64_t msecond() const { return _msecond; };
		virtual void year(int64_t val) = 0;
		virtual void month(int64_t val) = 0;
		virtual void day(int64_t val) = 0;
		virtual void hour(int64_t val) = 0;
		virtual void minute(int64_t val) = 0;
		virtual void second(int64_t val) = 0;
		virtual void msecond(int64_t val) = 0;

		virtual int64_t years() const = 0;
		virtual int64_t months() const = 0;
		virtual int64_t days() const = 0;
		virtual int64_t hours() const = 0;
		virtual int64_t minutes() const = 0;
		virtual int64_t seconds() const = 0;
		virtual int64_t mseconds() const = 0;

		virtual string str() const = 0;

	protected:
		int64_t _values[7];
		int64_t &_year = _values[0];
		int64_t &_month = _values[1];
		int64_t &_day = _values[2];
		int64_t &_hour = _values[3];
		int64_t &_minute = _values[4];
		int64_t &_second = _values[5];
		int64_t &_msecond = _values[6];
	};

	class freetime : public time
	{
	public:
		using time::day;
		using time::hour;
		using time::minute;
		using time::month;
		using time::msecond;
		using time::second;
		using time::year;
		freetime(int year = 0, int month = 0, int day = 0, int hour = 0, int minute = 0, int second = 0, int msecond = 0) : time(year, month, day, hour, minute, second, msecond){};
		freetime(const freetime &) = default;
		freetime(freetime &&) = default;

		void year(const int64_t val);
		void month(const int64_t val);
		void day(const int64_t val);
		void hour(const int64_t val);
		void minute(const int64_t val);
		void second(const int64_t val);
		void msecond(const int64_t val);

		int64_t years() const;
		int64_t months() const;
		int64_t days() const;
		int64_t hours() const;
		int64_t minutes() const;
		int64_t seconds() const;
		int64_t mseconds() const;

		freetime operator+(const freetime &t2) const;
		freetime &operator+=(const freetime &t2);
		freetime operator-(const freetime &t2) const;
		freetime &operator-=(const freetime &t2);
		freetime &add(const freetime &t2);
		freetime &add(const freetime *pt2);
		freetime &sub(const freetime &t2);
		freetime &sub(const freetime *pt2);

		void sim();

		string str() const;
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
		using time::day;
		using time::hour;
		using time::minute;
		using time::month;
		using time::msecond;
		using time::second;
		using time::year;
		realtime(int year, int month = -1, int day = -1, int hour = -1, int minute = -1, int second = -1, int msecond = -1) : time(year, month, day, hour, minute, second, msecond)
		{
			check();
		}
	};

	// 	realevel get_level() const;

	// 	// realevel get_level() const
	// 	//{
	// 	//	if (rlevel != realevel::UNKNOWN)
	// 	//		return rlevel;
	// 	//	else
	// 	//		throw(std::runtime_error(""));
	// 	// };

	// 	void year(const int64_t val)
	// 	{
	// 		_values[0] = val;
	// 		sim();
	// 	};
	// 	void month(const int64_t val)
	// 	{
	// 		_values[1] = val;
	// 		sim();
	// 	};
	// 	void day(const int64_t val)
	// 	{
	// 		_values[2] = val;
	// 		sim();
	// 	};
	// 	void hour(const int64_t val)
	// 	{
	// 		_values[3] = val;
	// 		sim();
	// 	};
	// 	void minute(const int64_t val)
	// 	{
	// 		_values[4] = val;
	// 		sim();
	// 	};
	// 	void second(const int64_t val)
	// 	{
	// 		_values[5] = val;
	// 		sim();
	// 	};
	// 	void msecond(const int64_t val)
	// 	{
	// 		_values[6] = val;
	// 		sim();
	// 	};
	// 	int64_t years() const;
	// 	int64_t months() const;
	// 	int64_t days() const;
	// 	int64_t hours() const;
	// 	int64_t minutes() const;
	// 	int64_t seconds() const;
	// 	int64_t mseconds() const;

	// 	realtime &operator+=(const freetime &itv);
	// 	realtime operator+(const freetime &itv) const;

	// 	realtime &operator-=(const freetime &itv);
	// 	realtime operator-(const freetime &itv) const;
	// 	freetime operator-(const realtime &real) const;

	// 	static int get_days_from_ym(int year, int month);
	// 	static bool isLeap(int year);

	// 	string str();
	// 	void sim();
	// 	int64_t stamp() const;

	// 	static int64_t countLeap(long year1, long year2, bool leftOC = true, bool rightOC = true);
	// 	static int get_jdays(int month, int day, int year = 1);

	// private:
	// 	mutable realevel rlevel = realevel::UNKNOWN;
	// 	void check()
	// 	{
	// 		// std::cout << static_cast<int>(get_level()) << std::endl;
	// 		// std::cout << "what?????" << std::endl;
	// 		if (get_level() >= realevel::MONTH && month() <= 0 || month() >= 13)
	// 			throw(std::runtime_error(""));
	// 		if (get_level() >= realevel::DAY && (day() <= 0 || day() > realtime::get_days_from_ym(year(), month())))
	// 			throw(std::runtime_error(""));
	// 		if (get_level() >= realevel::HOUR && (hour() < 0 || hour() >= 24))
	// 			throw(std::runtime_error(""));
	// 		if (get_level() >= realevel::MINUTE && (minute() < 0 || minute() >= 60))
	// 			throw(std::runtime_error(""));
	// 		if (get_level() >= realevel::SECOND && (second() < 0 || second() >= 60))
	// 			throw(std::runtime_error(""));
	// 		if (get_level() >= realevel::MSECOND && (msecond() < 0 || msecond() >= 1000))
	// 			throw(std::runtime_error(""));
	// 	}
	// };

	// class abstime : time
	// {};
};
