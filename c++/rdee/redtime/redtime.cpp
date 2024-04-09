#include <stdexcept>
#include <iostream>
#include <climits>
#include <cassert>
#include "redtime.h"

namespace redtime
{
	time& time::operator=(const time& t)
	{
		for (int i = 0; i < 7; i++)
			_values[i] = t._values[i];
		return *this;
	}
}

namespace redtime //@sk exp for freetime
{
	freetime::freetime(std::map<realevel, int64_t>&& timedefs)
	{
		for (const auto& kv : timedefs)
		{
			_values[static_cast<int>(kv.first)] = kv.second;
		}
	}

	freetime& freetime::year(const int64_t val)
	{
		_year = val;
		return *this;
	}
	freetime& freetime::month(const int64_t val)
	{
		_month = val;
		return *this;
	}
	freetime& freetime::day(const int64_t val)
	{
		_day = val;
		return *this;
	}
	freetime& freetime::hour(const int64_t val)
	{
		_hour = val;
		return *this;
	}
	freetime& freetime::minute(const int64_t val)
	{
		_minute = val;
		return *this;
	}
	freetime& freetime::second(const int64_t val)
	{
		_second = val;
		return *this;
	}
	freetime& freetime::msecond(const int64_t val)
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

	freetime& freetime::operator+=(const freetime& t2)
	{
		for (int i = 0; i < 7; i++)
			_values[i] += t2._values[i];
		return *this;
	}

	freetime freetime::operator+(const freetime& t2) const
	{
		freetime t6 = *this;
		t6 += t2;
		return t6;
	}

	realtime freetime::operator+(const realtime& real) const
	{
		return real + *this;
	}

	freetime& freetime::operator-=(const freetime& t2)
	{
		for (int i = 0; i < 7; i++)
			_values[i] -= t2._values[i];
		return *this;
	}

	freetime freetime::operator-(const freetime& t2) const
	{
		freetime t6 = *this;
		t6 -= t2;
		return t6;
	}

	freetime& freetime::operator=(const freetime& frt)
	{
		time::operator=(frt);
		return *this;
	}

	freetime& freetime::add(const freetime& t2)
	{
		*this += t2;
		return *this;
	}

	freetime& freetime::add(const freetime* pt2)
	{
		*this += *pt2;
		return *this;
	}

	freetime& freetime::sub(const freetime& t2)
	{
		*this -= t2;
		return *this;
	}

	freetime& freetime::sub(const freetime* pt2)
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
			throw(std::runtime_error("Wrong hour: " + std::to_string(_hour)));
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

	realtime& realtime::year(const int64_t val)
	{
		_year = val;
		if (_timescale < realevel::YEAR)
			set_timescale();
		check(realevel::YEAR);
		return *this;
	}
	realtime& realtime::month(const int64_t val)
	{
		_month = val;
		if (_timescale == realevel::YEAR)
			set_timescale();
		check(realevel::MONTH);
		return *this;
	}
	realtime& realtime::day(const int64_t val)
	{
		_day = val;
		if (_timescale == realevel::MONTH)
			set_timescale();
		else if (_timescale < realevel::MONTH)
			throw(std::runtime_error(""));
		check(realevel::DAY);
		return *this;
	}
	realtime& realtime::hour(const int64_t val)
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
	realtime& realtime::minute(const int64_t val)
	{
		_minute = val;
		if (_timescale == realevel::HOUR)
			set_timescale();
		else if (_timescale < realevel::HOUR)
			throw(std::runtime_error(""));
		check(realevel::MINUTE);
		return *this;
	}
	realtime& realtime::second(const int64_t val)
	{
		_second = val;
		if (_timescale == realevel::MINUTE)
			set_timescale();
		else if (_timescale < realevel::MINUTE)
			throw(std::runtime_error(""));
		check(realevel::SECOND);
		return *this;
	}
	realtime& realtime::msecond(const int64_t val)
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
		const static int mdays[] = { 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };
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

	realtime& realtime::operator+=(const freetime& itv)
	{
		for (int i = 0; i < 7; i++)
			if (static_cast<int>(_timescale) >= i)
				_values[i] += itv._values[i];
		// std::cout << str() << std::endl;
		sim();
		// std::cout << str() << std::endl;

		return *this;
	}

	realtime realtime::operator+(const freetime& itv) const
	{
		realtime real2 = *this;
		real2 += itv;
		return real2;
	}

	realtime& realtime::operator-=(const freetime& itv)
	{
		for (int i = 0; i < 7; i++)
			if (static_cast<int>(_timescale) >= i)
				_values[i] -= itv._values[i];
		sim();

		return *this;
	}

	realtime realtime::operator-(const freetime& itv) const
	{
		realtime real2 = *this;
		real2 -= itv;
		return real2;
	}

	freetime realtime::operator-(const realtime& real) const
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

	bool realtime::operator<(const realtime& real) const
	{

		for (int i = 0; i < 7; i++)
		{
			if (_values[i] >= real._values[i])
				return false;
		}
		return true;
	}
	bool realtime::operator>(const realtime& real) const
	{
		for (int i = 0; i < 7; i++)
		{
			if (_values[i] <= real._values[i])
				return false;
		}
		return true;
	}
	bool realtime::operator==(const realtime& real) const
	{
		for (int i = 0; i < 7; i++)
		{
			if (_values[i] != real._values[i])
				return false;
		}
		return true;
	}

	bool realtime::operator!=(const realtime& real) const
	{
		return !(*this == real);
	}
	bool realtime::operator<=(const realtime& real) const
	{
		for (int i = 0; i < 7; i++)
		{
			if (_values[i] > real._values[i])
				return false;
		}
		return true;
	}
	bool realtime::operator>=(const realtime& real) const
	{
		for (int i = 0; i < 7; i++)
		{
			if (_values[i] < real._values[i])
				return false;
		}
		return true;
	}

	realtime& realtime::operator=(const realtime& rt)
	{
		time::operator=(rt);
		_timescale = rt._timescale;
		return *this;
	}

	realtime realtime::rebase(realevel ts) const
	{
		/*
		This function aims to change the timescale. For dimension reduction, just set the dropped dimension values to -1;
		For dimension elevetion, use default: month=1, day=1, hour/minute/second=0
		*/
		if (static_cast<int>(ts) < 0)
			throw(std::runtime_error("(realtime::rebase) Error! cannot rebase to a non-concrete timescale!"));

		realtime rt6 = *this;
		static int v_default[7] = { 1900, 1, 1, 0, 0, 0, 0 };
		if (static_cast<int>(ts) <= static_cast<int>(_timescale))
		{
			//@sk dimensional reduction
			for (int i = static_cast<int>(ts) + 1; i < 7; i++)
				rt6._values[i] = -1;
		}
		else
		{
			for (int i = static_cast<int>(_timescale) + 1; i <= static_cast<int>(ts); i++)
				rt6._values[i] = v_default[i];
		}
		rt6.set_timescale();
		return rt6;
	}

	realtimeseries realtime::rebase2rts(realevel ts) const
	{
		if (static_cast<int>(ts) < 0)
			throw(std::runtime_error("(realtime::rebase) Error! cannot rebase to a non-concrete timescale!"));

		// std::cout << "(rebase2rts) [D] ts=" << static_cast<int>(ts) << std::endl;

		realtimeseries rts;
		static int v_default[7] = { 1900, 1, 1, 0, 0, 0, 0 };
		if (static_cast<int>(ts) == static_cast<int>(_timescale))
		{
			rts.add(*this);
		}
		else if (static_cast<int>(ts) < static_cast<int>(_timescale))
		{
			//@sk dimensional reduction
			realtime rt6 = *this;
			for (int i = static_cast<int>(ts) + 1; i < 7; i++)
				rt6._values[i] = -1;
			rts.add(rt6);
		}
		else if (static_cast<int>(ts) > static_cast<int>(_timescale))
		{
			switch (_timescale)
			{
			case redtime::realevel::YEAR:
				for (int m = 1; m <= 12; m++)
					rts.add(realtime(_year, m).rebase2rts(ts));
				break;
			case redtime::realevel::MONTH:
				for (int i = 1; i <= realtime::get_days_from_ym(_year, _month); i++)
					rts.add(realtime(_year, _month, i).rebase2rts(ts));
				break;
			case redtime::realevel::DAY:
				for (int i = 0; i < 24; i++)
					rts.add(realtime(_year, _month, _day, i).rebase2rts(ts));
				break;
			case redtime::realevel::HOUR:
				for (int i = 0; i < 60; i++)
					rts.add(realtime(_year, _month, _day, _hour, i).rebase2rts(ts));
				break;
			case redtime::realevel::MINUTE:
				for (int i = 0; i < 60; i++)
					rts.add(realtime(_year, _month, _day, _hour, _minute, i).rebase2rts(ts));
				break;
			case redtime::realevel::SECOND:
				throw(std::runtime_error("(realtime::rebase2rts) Error! rebase to millisecond is not supported"));
				break;
			default:
				break;
			}
			return rts;
		}

		return rts;
	}

}

namespace redtime
{
	realtimeseries& realtimeseries::add(const realtime& rt)
	{
		data.push_back(rt);
		if (data.size() == 1)
			_timescale = rt.get_timescale();
		else if (_timescale != rt.get_timescale())
			throw(std::runtime_error("(realtimeseries::add) Error! Trying to add a realtime with different timescale"));

		return *this;
	}

	realtimeseries& realtimeseries::add(const realtimeseries& rts)
	{
		for (const realtime& rt : rts.data)
			add(rt);
		return *this;
	}

	realtimeseries& realtimeseries::pop()
	{
		data.pop_back();
		if (data.empty())
			_timescale = realevel::UNKNOWN;
		return *this;
	}

	realtimeseries::realtimeseries(const realtime& real1, const realtime& real2, const freetime& frt)
	{
		/*
		This static function aims to generate a vector of realtime based on start, end, and delta time
		*/
		if (real1 > real2 || !frt.is_positive())
			throw(std::runtime_error("(redtime::realtimeseries::init) Error! Requires real1 < real2 now."));

		if (real1 + frt == real1)
			throw(std::runtime_error("(redtime::realtimeseries::init) Error! interval time scale maks nonsense for input realtime."));

		if (real1.get_timescale() != real2.get_timescale())
			throw(std::runtime_error("(redtime::realtimeseries::init) Error! realtimeseries only works for realtime objects with the same timescale!"));

		// std::vector<realtime> rstlist;
		//  std::cout << "start loop" << std::endl;
		realtime realT = real1;

		// interval = frt;
		_timescale = real1.get_timescale();

		while (realT <= real2)
		{
			data.push_back(realT);
			// std::cout << rstlist[0].str() << std::endl;
			// std::cout << rstlist.size() << std::endl;
			realT += frt;
		}
		// std::cout << rstlist[0]._values[0] << ' ' << rstlist[0]._month << ' ' << rstlist[0]._day << ' ' << rstlist[0]._hour << rstlist[0]._minute << rstlist[0]._second << rstlist[0]._msecond << std::endl;
		// std::cout << rstlist[0].str() << std::endl;
	}

	//@ <function>
	//@  This function aims to do the dimension-reduction or dimension-elevation along time dimensions, i.e., YMdhms, for a series of realtimes (class realtimeseries)
	//@ <param name="ts" meaning="target timescale" desc="target timescale, can be any of one from realevel::YEAR to realevel::SECOND"/>
	//@ <param name="unique" meaning="unique or not for results" desc="if set to true, repeated element in dimension-reduction operation will be ignored, since no repeated values will be created in dimension-elevation operation only if there exists the same realtimes in the original realtimeseries, which we may not want to alter"/>
	//@ <return decs="A new realtimeseries object"/>
	realtimeseries realtimeseries::rebase(realevel ts, bool unique)
	{
		//@ prepare
		//@ prepare.errorDetect exclude un-desgined conditions
		if (static_cast<int>(ts) < 0) //@branch not valid timescale
			throw(std::runtime_error("(realtimeseries::rebase) Error! cannot rebase to a non-concrete timescale!"));

		//@ prepare.varDef
		realtimeseries rts;
		static int v_default[7] = { 1900, 1, 1, 0, 0, 0, 0 };
		realtime rtT;

		//@ core handle different conditions based on ts and this->_timescale
		if (static_cast<int>(ts) <= static_cast<int>(_timescale)) //@branch ts <= _timescale, i.e., dimension reduction operation, this is simple
		{
			//@code.DRP loop each realtime, rebase & add
			for (const realtime& rt : data)
			{
				rtT = rt.rebase(ts); //@ exp drp for one realtime.
				if (!unique || (unique && !rts.data.empty() && rtT != rts.data.back())) //@branch exclude repeated realtime in unique=true
					rts.add(rtT);
			}
		}
		else //@branch ts > _timescale, i.e., dimension elevation operation, the heavy processing code is put in realtime::rebase2rts, See <function:realtime::rebase2rts>
		{
			//@core.DEP The logic is simple, i.e., add all corresponding rebase-DEP results for each element
			for (const realtime& rt : data)
				rts.add(rt.rebase2rts(ts));
		}
		//@return
		return rts;
	}
}
