#include <stdexcept>
#include <iostream>
#include <climits>
#include <cassert>
#include "redtime.h"

namespace redtime //@sk exp for freetime
{
	freetime::freetime(std::map<realevel, int64_t> &&timedefs)
	{
		for (const auto &kv : timedefs)
		{
			_values[static_cast<int>(kv.first)] = kv.second;
		}
	}

	freetime &freetime::year(const int64_t val)
	{
		_year = val;
		return *this;
	}
	freetime &freetime::month(const int64_t val)
	{
		_month = val;
		return *this;
	}
	freetime &freetime::day(const int64_t val)
	{
		_day = val;
		return *this;
	}
	freetime &freetime::hour(const int64_t val)
	{
		_hour = val;
		return *this;
	}
	freetime &freetime::minute(const int64_t val)
	{
		_minute = val;
		return *this;
	}
	freetime &freetime::second(const int64_t val)
	{
		_second = val;
		return *this;
	}
	freetime &freetime::msecond(const int64_t val)
	{
		_msecond = val;
		return *this;
	}

	string freetime::str() const
	{
		return std::to_string(_year) + "/" + std::to_string(_month) + "/" + std::to_string(_day) + " " + std::to_string(_hour) + ":" + std::to_string(_minute) + ":" + std::to_string(_second);
	}

	void freetime::sim()
	{
		//@sk core handle dhms
		int64_t seconds = _day * 86400 + _hour * 3600 + _minute * 60 + _second;
		if (seconds >= 0)
		{
			_day = seconds / 86400;
		}
		else
		{
			_day = (seconds - 86399) / 86400;
		}
		seconds -= _day * 86400;
		_hour = seconds / 3600;
		seconds -= hour() * 3600;
		_minute = seconds / 60;
		_second = seconds % 60;

		//@sk core handle year-month
		int64_t months = _year * 12 + _month;
		if (months < 0)
		{
			_year = (months - 11) / 12;
		}
		else
		{
			_year = months / 12;
		}
		_month = months - year() * 12;
	}

	int64_t freetime::years() const
	{
		freetime itv = *this;
		// std::cout << str() << std::endl;
		itv.sim(); //@sk exp make sure month() between 0 ~ 11
		// std::cout << str() << std::endl;

		// std::cout << _values << ' ' << &_month << ' ' << &_month << std::endl;
		// std::cout << itv._values << ' ' << &itv._month << ' ' << &itv._month << std::endl;
		return itv._year;
	}

	int64_t freetime::months() const
	{
		return _year * 12 + _month; //@sk exp for isolated months, doesn't need sim
	}

	int64_t freetime::days() const
	{
		freetime itv = *this;
		itv.sim();
		return itv._day;
	}
	int64_t freetime::hours() const
	{
		freetime itv = *this;
		itv.sim();
		return itv._day * 24 + itv._hour;
	}
	int64_t freetime::minutes() const
	{
		freetime itv = *this;
		itv.sim();
		return itv._day * 60 * 24 + itv._hour * 60 + itv._minute;
	}
	int64_t freetime::seconds() const
	{
		return _day * 86400 + _hour * 3600 + _minute * 60 + _second;
	}
	int64_t freetime::mseconds() const
	{
		return -1;
	}

	freetime &freetime::operator+=(const freetime &t2)
	{
		for (int i = 0; i < 7; i++)
			_values[i] += t2._values[i];
		return *this;
	}

	freetime freetime::operator+(const freetime &t2) const
	{
		freetime t6 = *this;
		t6 += t2;
		return t6;
	}

	realtime freetime::operator+(const realtime &real) const
	{
		return real + *this;
	}

	freetime &freetime::operator-=(const freetime &t2)
	{
		for (int i = 0; i < 7; i++)
			_values[i] -= t2._values[i];
		return *this;
	}

	freetime freetime::operator-(const freetime &t2) const
	{
		freetime t6 = *this;
		t6 -= t2;
		return t6;
	}

	freetime &freetime::add(const freetime &t2)
	{
		*this += t2;
		return *this;
	}

	freetime &freetime::add(const freetime *pt2)
	{
		*this += *pt2;
		return *this;
	}

	freetime &freetime::sub(const freetime &t2)
	{
		*this -= t2;
		return *this;
	}

	freetime &freetime::sub(const freetime *pt2)
	{
		*this -= *pt2;
		return *this;
	}

	bool freetime::is_empty() const
	{
		for (int64_t v : _values)
			if (v != 0)
				return false;
		return true;
	}

	bool freetime::is_positive() const
	{
		if (is_empty()) //@sdk branch exclude the boundary condition for empty time
			return false;
		return months() >= 0 && seconds() >= 0;
	}

}

namespace redtime
{

	void realtime::check(realevel ts)
	{
		// std::cout << "enter check: " << static_cast<int>(ts) << ' ' << static_cast<int>(_timescale) << std::endl;
		if (_timescale == realevel::UNKNOWN)
			throw(std::runtime_error("Cannot check an UNKNOWN-timescale realtime"));
		if (ts > _timescale)
			throw(std::runtime_error("Cannot check ts > object's timescale"));
		// std::cout << static_cast<int>(_timescale) << std::endl;
		if ((ts == realevel::MONTH || (ts == realevel::ALL && _timescale >= realevel::MONTH)) && month() <= 0 || month() >= 13)
			throw(std::runtime_error("Wrong month"));
		if ((ts == realevel::DAY || (ts == realevel::ALL && _timescale >= realevel::DAY)))
			if (_day < 1 || _day > realtime::get_days_from_ym(_year, _month))
				throw(std::runtime_error("Wrong day"));
		if ((ts == realevel::HOUR || (ts == realevel::ALL && _timescale >= realevel::HOUR)) && _hour < 0 || _hour >= 24)
			throw(std::runtime_error("Wrong hour"));
		if ((ts == realevel::MINUTE || (ts == realevel::ALL && _timescale >= realevel::MINUTE)) && _minute < 0 || _minute >= 60)
			throw(std::runtime_error("Wrong minute"));
		if ((ts == realevel::SECOND || (ts == realevel::ALL && _timescale >= realevel::SECOND)) && _second < 0 || _second >= 60)
			throw(std::runtime_error("Wrong second: " + std::to_string(_second)));
		if ((ts == realevel::MSECOND || (ts == realevel::ALL && _timescale >= realevel::MSECOND)) && _msecond < 0 || _msecond >= 1000)
			throw(std::runtime_error("Wrong millisecond"));
	}

	void realtime::set_timescale() const
	{
		int i;
		for (i = 0; i < 7; i++)
		{
			if (_values[i] < 0)
			{
				_timescale = static_cast<realevel>(i - 1); //@sk exp since the values for realevel::* are manuall orgnized
				break;
			}
		}
	};

	realevel realtime::get_timescale() const
	{
		return _timescale;
	}

	realtime &realtime::year(const int64_t val)
	{
		_year = val;
		if (_timescale < realevel::YEAR)
			set_timescale();
		check(realevel::YEAR);
		return *this;
	}
	realtime &realtime::month(const int64_t val)
	{
		_month = val;
		if (_timescale == realevel::YEAR)
			set_timescale();
		check(realevel::MONTH);
		return *this;
	}
	realtime &realtime::day(const int64_t val)
	{
		_day = val;
		if (_timescale == realevel::MONTH)
			set_timescale();
		else if (_timescale < realevel::MONTH)
			throw(std::runtime_error(""));
		check(realevel::DAY);
		return *this;
	}
	realtime &realtime::hour(const int64_t val)
	{
		_hour = val;
		if (_timescale == realevel::DAY)
			set_timescale();
		else if (_timescale < realevel::DAY)
			throw(std::runtime_error(""));
		// std::cout << "cp1" << std::endl;

		check(realevel::HOUR);
		return *this;
	}
	realtime &realtime::minute(const int64_t val)
	{
		_minute = val;
		if (_timescale == realevel::HOUR)
			set_timescale();
		else if (_timescale < realevel::HOUR)
			throw(std::runtime_error(""));
		check(realevel::MINUTE);
		return *this;
	}
	realtime &realtime::second(const int64_t val)
	{
		_second = val;
		if (_timescale == realevel::MINUTE)
			set_timescale();
		else if (_timescale < realevel::MINUTE)
			throw(std::runtime_error(""));
		check(realevel::SECOND);
		return *this;
	}
	realtime &realtime::msecond(const int64_t val)
	{
		_msecond = val;
		if (_timescale == realevel::SECOND)
			set_timescale();
		else if (_timescale < realevel::SECOND)
			throw(std::runtime_error(""));
		check(realevel::MSECOND);
		return *this;
	}

	int64_t realtime::years() const
	{
		return _year;
	}

	int64_t realtime::months() const
	{
		return (_year - 1) * 12 + _month;
	}

	int64_t realtime::days() const
	{
		int64_t rst_days = _day;
		// std::cout << seconds << std::endl;
		if (_year > 1)
			rst_days += ((_year - 1) * 365 + realtime::countLeap(1, _year - 1, true, false));
		rst_days += realtime::get_jdays(_month, 1, _year) - 1;
		return rst_days;
	}
	int64_t realtime::hours() const
	{
		return (days() - 1) * 24 + _hour;
	}
	int64_t realtime::minutes() const
	{
		return hours() * 60 + _minute;
	}
	int64_t realtime::seconds() const
	{
		return minutes() * 60 + _second;
	}
	int64_t realtime::mseconds() const
	{
		return -1;
	}

	int64_t realtime::stamp() const
	{
		switch (_timescale)
		{
		case realevel::YEAR:
			return years();
			break;
		case realevel::MONTH:
			return months();
			break;
		case realevel::DAY:
			return days();
			break;
		case realevel::HOUR:
			return hours();
			break;
		case realevel::MINUTE:
			return minutes();
			break;
		case realevel::SECOND:
			return seconds();
			break;
		default:
			break;
		}
		throw(std::runtime_error("Wrong timescale!"));
	}

	bool realtime::isLeap(int year)
	{
		assert(year != 0);
		if (year % 4 != 0)
			return false;
		else if (year % 100 != 0)
			return true;
		else if (year % 400 == 0)
			return true;
		else
			return false;
	}

	int realtime::get_days_from_ym(int year, int month)
	{
		// std::cout << year << month << std::endl;

		if (!(year != 0 && month > 0 && month <= 12))
			throw(std::runtime_error("year = " + std::to_string(year) + ", month = " + std::to_string(month)));
		const static int mdays[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
		if (isLeap(year) && month == 2)
			return 29;
		else
			return mdays[month - 1]; //@sk hint Do not forget "-1"
	}

	string realtime::str() const
	{
		string rst = std::to_string(year());
		// std::cout << "rst=" << rst << std::endl;
		// std::cout << "_year=" << _year << std::endl;
		// std::cout << "_values[0]=" << _values[0] << std::endl;

		if (_timescale == realevel::YEAR)
			return rst;

		rst += ("/" + std::to_string(month()));
		if (_timescale == realevel::MONTH)
			return rst;

		rst += ("/" + std::to_string(day()));
		if (_timescale == realevel::DAY)
			return rst;

		rst += (" " + std::to_string(hour()));
		if (_timescale == realevel::HOUR)
			return rst;

		rst += (":" + std::to_string(minute()));
		if (_timescale == realevel::MINUTE)
			return rst;

		rst += (":" + std::to_string(second()));
		return rst;
	}

	int64_t realtime::countLeap(long year1, long year2, bool with_left, bool with_right)
	{
		if (year1 > year2)
			return countLeap(year2, year1, with_right, with_left);
		auto countLeapFrom0 = [](long yr, bool with_boundary)
		{
			yr = abs(yr);
			return yr / 4 - yr / 100 + yr / 400 + (with_boundary ? 0 : -1) * realtime::isLeap(yr);
		};

		return countLeapFrom0(year2, with_right) * (year2 > 0 ? 1 : -1) - countLeapFrom0(year1, with_left) * (year1 > 0 ? 1 : -1);
	}

	int realtime::get_jdays(int month, int day, int year)
	{
		bool isLeap = realtime::isLeap(year);
		int jdays = 0;
		for (int i = 1; i < month; i++)
		{
			jdays += realtime::get_days_from_ym(year, i);
		}
		jdays += day;
		return jdays;
	}

	void realtime::sim()
	{
		assert(_timescale != realevel::UNKNOWN);

		if (_timescale == realevel::YEAR) //@sk exp branch only contain year, no need for simplification
			return;

		//@sk core handel year-month logic separately
		int64_t _months = year() * 12 + month();
		if (_months <= 0)
		{
			_year = (_months - 12) / 12;
		}
		else
		{
			_year = (_months - 1) / 12;
		}
		_month = _months - year() * 12;
		assert(month() > 0 && month() < 13);

		if (_timescale == realevel::MONTH)
			return;
		// std::cout << str() << std::endl;

		// sk ?? make a fraud for convinence, need to be turned back after
		for (int i = static_cast<int>(_timescale) + 1; i < 7; i++)
			_values[i] = 0;

		int64_t seconds = (_day - 1) * 86400 + _hour * 3600 + _minute * 60 + _second;
		if (seconds >= 0)
		{
			_day = seconds / 86400;
		}
		else
		{
			_day = (seconds - 86399) / 86400;
		}
		seconds -= _day * 86400;
		_hour = seconds / 3600;
		seconds -= hour() * 3600;
		_minute = seconds / 60;
		_second = seconds % 60;
		_day += 1;

		//@sk core build a bridge between year-month and day
		if (_day <= 0)
		{										  //@sk branch convert negative day to positive day, in yearly operation
			int64_t nyears_n2p = -_day / 366 + 1; //@sk exp years that makes day be positive
			int64_t ndays_n2p = nyears_n2p * 365 + realtime::countLeap(_year - nyears_n2p, _year, _month > 2 ? false : true, _month > 2 ? true : false);
			_year -= nyears_n2p;
			_day += ndays_n2p;
		}

		//@sk core reduce excessive day
		//@sk part1 reduce very large day to near-close range in one step
		int64_t nyears_p20 = _day / 366;
		if (nyears_p20 > 0)
		{
			int64_t ndays_p20 = nyears_p20 * 365 + realtime::countLeap(_year, _year + nyears_p20, _month > 2 ? false : true, _month > 2 ? true : false);
			_year += nyears_p20;
			_day -= ndays_p20;
		}

		//@sk part2 handle left months
		while (_day > realtime::get_days_from_ym(_year, _month))
		{
			_day -= realtime::get_days_from_ym(_year, _month);
			_month += 1;
			if (_month == 0)
			{
				_month = 12;
				_year -= 1;
				assert(_year > 0);
			}
			else if (_month == 13)
			{
				_month = 1;
				_year += 1;
			}
		}

		// sk ?? restore the fraud
		for (int i = static_cast<int>(_timescale) + 1; i < 7; i++)
		{
			_values[i] = -1;
		}

		return;
	}

	realtime &realtime::operator+=(const freetime &itv)
	{
		for (int i = 0; i < 7; i++)
			if (static_cast<int>(_timescale) >= i)
				_values[i] += itv._values[i];
		// std::cout << str() << std::endl;
		sim();
		// std::cout << str() << std::endl;

		return *this;
	}

	realtime realtime::operator+(const freetime &itv) const
	{
		realtime real2 = *this;
		real2 += itv;
		return real2;
	}

	realtime &realtime::operator-=(const freetime &itv)
	{
		for (int i = 0; i < 7; i++)
			if (static_cast<int>(_timescale) >= i)
				_values[i] -= itv._values[i];
		sim();

		return *this;
	}

	realtime realtime::operator-(const freetime &itv) const
	{
		realtime real2 = *this;
		real2 -= itv;
		return real2;
	}

	freetime realtime::operator-(const realtime &real) const
	{
		realtime real2 = *this;

		if (this->_timescale != real._timescale)
		{
			throw(std::logic_error("Cannot substract a realtime with different time level!"));
		}

		int64_t stamp1 = stamp(), stamp2 = real.stamp();
		if (stamp1 == stamp2)
			return freetime();

		// freetime itv(std::map<realevel, int64_t>{{_timescale, stamp1 - stamp2}});
		// itv.sim();
		// return itv;
		return freetime(std::map<realevel, int64_t>{{_timescale, stamp1 - stamp2}});
	}

	bool realtime::operator<(const realtime &real) const
	{

		for (int i = 0; i < 7; i++)
		{
			if (_values[i] >= real._values[i])
				return false;
		}
		return true;
	}
	bool realtime::operator>(const realtime &real) const
	{
		for (int i = 0; i < 7; i++)
		{
			if (_values[i] <= real._values[i])
				return false;
		}
		return true;
	}
	bool realtime::operator==(const realtime &real) const
	{
		for (int i = 0; i < 7; i++)
		{
			if (_values[i] != real._values[i])
				return false;
		}
		return true;
	}

	bool realtime::operator!=(const realtime &real) const
	{
		return !(*this == real);
	}
	bool realtime::operator<=(const realtime &real) const
	{
		for (int i = 0; i < 7; i++)
		{
			if (_values[i] > real._values[i])
				return false;
		}
		return true;
	}
	bool realtime::operator>=(const realtime &real) const
	{
		for (int i = 0; i < 7; i++)
		{
			if (_values[i] < real._values[i])
				return false;
		}
		return true;
	}

	std::vector<realtime> realtime::range(realtime real1, const realtime &real2, const freetime &frt)
	{
		/*
		This static function aims to generate a vector of realtime based on start, end, and delta time
		*/
		if (real1 > real2 || !frt.is_positive())
			throw(std::runtime_error("(redtime::realtime::range) Error! Requires real1 < real2 now."));

		if (real1 + frt == real1)
			throw(std::runtime_error("(redtime::realtime::range) Error! interval time scale maks nonsense for input realtime."));

		std::vector<realtime> rstlist;
		// std::cout << "start loop" << std::endl;

		while (real1 <= real2)
		{
			rstlist.push_back(real1);
			// std::cout << rstlist[0].str() << std::endl;
			// std::cout << rstlist.size() << std::endl;
			real1 += frt;
		}
		// std::cout << rstlist[0]._values[0] << ' ' << rstlist[0]._month << ' ' << rstlist[0]._day << ' ' << rstlist[0]._hour << rstlist[0]._minute << rstlist[0]._second << rstlist[0]._msecond << std::endl;
		// std::cout << rstlist[0].str() << std::endl;

		return rstlist;
	}

}
