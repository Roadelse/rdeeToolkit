#pragma once

#include <iostream>
#include <cstdint>
#include <climits>
#include <cassert>
#include <string>
#include <map>
#include <vector>

using std::string;

namespace redtime
{
	class time
	{
	public:
		time(int year = 0, int month = 0, int day = 0, int hour = 0, int minute = 0, int second = 0, int msecond = 0) : _values{year, month, day, hour, minute, second, msecond}, _year(_values[0]), _month(_values[1]), _day(_values[2]), _hour(_values[3]), _minute(_values[4]), _second(_values[5]), _msecond(_values[6]){};
		time(const time &frt) : _values{frt._values[0], frt._values[1], frt._values[2], frt._values[3], frt._values[4], frt._values[5], frt._values[6]}, _year(_values[0]), _month(_values[1]), _day(_values[2]), _hour(_values[3]), _minute(_values[4]), _second(_values[5]), _msecond(_values[6]){};
		time(time &&other) noexcept : _values{other._year, other._month, other._day, other._hour, other._minute, other._second, other._msecond}, _year(_values[0]), _month(_values[1]), _day(_values[2]), _hour(_values[3]), _minute(_values[4]), _second(_values[5]), _msecond(_values[6]){};

		int64_t year() const { return _year; };
		int64_t month() const { return _month; };
		int64_t day() const { return _day; };
		int64_t hour() const { return _hour; };
		int64_t minute() const { return _minute; };
		int64_t second() const { return _second; };
		int64_t msecond() const { return _msecond; };
		virtual time &year(int64_t val) = 0;
		virtual time &month(int64_t val) = 0;
		virtual time &day(int64_t val) = 0;
		virtual time &hour(int64_t val) = 0;
		virtual time &minute(int64_t val) = 0;
		virtual time &second(int64_t val) = 0;
		virtual time &msecond(int64_t val) = 0;

		virtual int64_t years() const = 0;
		virtual int64_t months() const = 0;
		virtual int64_t days() const = 0;
		virtual int64_t hours() const = 0;
		virtual int64_t minutes() const = 0;
		virtual int64_t seconds() const = 0;
		virtual int64_t mseconds() const = 0;

		virtual string str() const = 0;

		time& operator=(const time& t);

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

	enum class realevel
	{
		UNKNOWN = -1,
		YEAR = 0,
		MONTH = 1,
		DAY = 2,
		HOUR = 3,
		MINUTE = 4,
		SECOND = 5,
		MSECOND = 6,
		ALL = -2
	};

	class realtime;
	class realtimeseries;

	class freetime : public time
	{
	public:
		friend class realtime;
		using time::day;
		using time::hour;
		using time::minute;
		using time::month;
		using time::msecond;
		using time::second;
		using time::year;
		freetime(int year = 0, int month = 0, int day = 0, int hour = 0, int minute = 0, int second = 0, int msecond = 0) : time(year, month, day, hour, minute, second, msecond){};
		freetime(std::map<realevel, int64_t> &&timedefs);
		freetime(const freetime &) = default;
		freetime(freetime &&) = default;

		freetime &year(const int64_t val);
		freetime &month(const int64_t val);
		freetime &day(const int64_t val);
		freetime &hour(const int64_t val);
		freetime &minute(const int64_t val);
		freetime &second(const int64_t val);
		freetime &msecond(const int64_t val);

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

		realtime operator+(const realtime &real) const;

		void sim();

		string str() const;
		bool is_positive() const;
		bool is_empty() const;

		freetime& operator=(const freetime& frt);
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
			set_timescale();
			check();
		}
		realtime() = default;
		realtime(const realtime &) = default;
		realtime(realtime &&) = default;

		realevel get_timescale() const;

		realtime &year(const int64_t val);
		realtime &month(const int64_t val);
		realtime &day(const int64_t val);
		realtime &hour(const int64_t val);
		realtime &minute(const int64_t val);
		realtime &second(const int64_t val);
		realtime &msecond(const int64_t val);

		int64_t years() const;
		int64_t months() const;
		int64_t days() const;
		int64_t hours() const;
		int64_t minutes() const;
		int64_t seconds() const;
		int64_t mseconds() const;

		int64_t stamp() const;

		static int get_days_from_ym(int year, int month);
		static bool isLeap(int year);

		string str() const;

		static int64_t countLeap(long year1, long year2, bool leftOC = true, bool rightOC = true);
		static int get_jdays(int month, int day, int year = 1);

		void sim();

		realtime &operator+=(const freetime &itv);
		realtime operator+(const freetime &itv) const;

		realtime &operator-=(const freetime &itv);
		realtime operator-(const freetime &itv) const;
		freetime operator-(const realtime &real) const;

		bool operator<(const realtime &real) const;
		bool operator>(const realtime &real) const;
		bool operator==(const realtime &real) const;
		bool operator!=(const realtime &real) const;
		bool operator<=(const realtime &real) const;
		bool operator>=(const realtime &real) const;

		realtime& operator=(const realtime&);

		//static std::vector<realtime> range(realtime, const realtime &, const freetime &);

		realtime rebase(realevel ts) const;
		realtimeseries rebase2rts(realevel ts) const;

	private:
		mutable realevel _timescale;
		void check(realevel ts = realevel::ALL);
		void set_timescale() const;
	};

	class realtimeseries {
	public:
		//@sk fields
		//freetime interval;
		std::vector<realtime> data;

		//@sk methods
		//@sk methods.init
		realtimeseries() = default;
		realtimeseries(const realtime& real1, const realtime& real2, const freetime& frt);
		//@sk methods.final
		//~realtimeseries() { data.clear(); };  // unnecessary

		realevel get_timescale() const { return _timescale; };


		//@sk methods.??
		realtimeseries& add(const realtime&);
		realtimeseries& add(const realtimeseries&);
		realtimeseries& pop();
		realtimeseries rebase(realevel, bool unique = true);

	private:
		realevel _timescale = realevel::UNKNOWN;
	};

}
