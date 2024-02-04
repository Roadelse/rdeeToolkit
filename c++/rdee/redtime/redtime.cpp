﻿#include <stdexcept>
#include <iostream>
#include <climits>
#include <cassert>
#include "redtime.h"

namespace redtime //@sk exp for freetime
{
	void freetime::year(const int64_t val)
	{
		_year = val;
	}
	void freetime::month(const int64_t val)
	{
		_month = val;
	}
	void freetime::day(const int64_t val)
	{
		_day = val;
	}
	void freetime::hour(const int64_t val)
	{
		_hour = val;
	}
	void freetime::minute(const int64_t val)
	{
		_minute = val;
	}
	void freetime::second(const int64_t val)
	{
		_second = val;
	}
	void freetime::msecond(const int64_t val)
	{
		_msecond = val;
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

		// std::cout << _values << ' ' << &_month << ' ' << &_values[1] << std::endl;
		// std::cout << itv._values << ' ' << &itv._month << ' ' << &itv._values[1] << std::endl;
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

}

// bool realtime::isLeap(int year)
// {
// 	assert(year != 0);
// 	if (year % 4 != 0)
// 		return false;
// 	else if (year % 100 != 0)
// 		return true;
// 	else if (year % 400 == 0)
// 		return true;
// 	else
// 		return false;
// }

// int realtime::get_days_from_ym(int year, int month)
// {
// 	// std::cout << year << month << std::endl;
// 	assert(year != 0 && month > 0 && month <= 12);
// 	const static int mdays[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
// 	if (isLeap(year) && month == 2)
// 		return 29;
// 	else
// 		return mdays[month - 1]; //@sk hint Do not forget "-1"
// }

// string realtime::str()
// {
// 	string rst = std::to_string(year());
// 	if (get_level() == realevel::YEAR)
// 		return rst;

// 	rst += ("/" + std::to_string(month()));
// 	if (get_level() == realevel::MONTH)
// 		return rst;

// 	rst += ("/" + std::to_string(day()));
// 	if (get_level() == realevel::DAY)
// 		return rst;

// 	rst += (" " + std::to_string(hour()));
// 	if (get_level() == realevel::HOUR)
// 		return rst;

// 	rst += (":" + std::to_string(minute()));
// 	if (get_level() == realevel::MINUTE)
// 		return rst;

// 	rst += (":" + std::to_string(second()));
// 	return rst;
// }

// realevel realtime::get_level() const
// {
// 	if (rlevel != realevel::UNKNOWN)
// 		return rlevel;
// 	int i;
// 	for (i = 0; i < 7; i++)
// 	{
// 		if (_values[i] < 0)
// 		{
// 			rlevel = static_cast<realevel>(i - 1); //@sk exp since the values for realevel::* are manuall orgnized
// 			break;
// 		}
// 	}
// 	return rlevel;
// }

// realtime &realtime::operator+=(const freetime &itv)
// {
// 	int myLevel = static_cast<int>(get_level());
// 	for (int i = 0; i < 7; i++)
// 		if (myLevel >= i)
// 			_values[i] += itv._values[i];
// 	// std::cout << str() << std::endl;
// 	sim();
// 	// std::cout << str() << std::endl;

// 	return *this;
// }

// realtime realtime::operator+(const freetime &itv) const
// {
// 	realtime real2 = *this;
// 	real2 += itv;
// 	return real2;
// }

// realtime &realtime::operator-=(const freetime &itv)
// {
// 	int myLevel = static_cast<int>(get_level());
// 	for (int i = 0; i < 7; i++)
// 		if (myLevel >= i)
// 			_values[i] -= itv._values[i];
// 	sim();

// 	return *this;
// }

// realtime realtime::operator-(const freetime &itv) const
// {
// 	realtime real2 = *this;
// 	real2 -= itv;
// 	return real2;
// }

// freetime realtime::operator-(const realtime &real) const
// {
// 	if (this->get_level() != real.get_level())
// 	{
// 		throw(std::logic_error("Cannot substract a realtime with different time level!"));
// 	}

// 	int64_t stamp1 = this->stamp(), stamp2 = real.stamp();
// 	freetime itv(0, 0, 0, 0, 0, stamp1 - stamp2);
// 	itv.sim();

// 	return itv;
// }

// void realtime::sim()
// {
// 	int myLevel = static_cast<int>(get_level());
// 	assert(get_level() != realevel::UNKNOWN);

// 	if (get_level() == realevel::YEAR) //@sk exp branch only contain year, no need for simplification
// 		return;

// 	// sim_dhms();  //@sk exp simplify day-hour-minute-second first in uniform api

// 	//@sk core handel year-month logic separately
// 	int64_t _months = year() * 12 + month();
// 	if (_months <= 0)
// 	{
// 		year((_months - 12) / 12);
// 	}
// 	else
// 	{
// 		year((_months - 1) / 12);
// 	}
// 	month(_months - year() * 12);
// 	assert(month() > 0 && month() < 13);

// 	if (get_level() == realevel::MONTH)
// 		return;
// 	// std::cout << str() << std::endl;

// 	// sk ?? make a fraud for convinence, need to be turned back after
// 	for (int i = myLevel + 1; i < 7; i++)
// 	{
// 		_values[i] = 0;
// 	}

// 	sim_dhms();

// 	//@sk core build a bridge between year-month and day
// 	if (_values[2] < 0)
// 	{												//@sk branch convert negative day to positive day, in yearly operation
// 		int64_t nyears_n2p = -_values[2] / 366 + 1; //@sk exp years that makes day be positive
// 		int64_t ndays_n2p = nyears_n2p * 365 + realtime::countLeap(_values[0] - nyears_n2p, _values[0], _values[1] > 2 ? false : true, _values[1] > 2 ? true : false);
// 		_values[0] -= nyears_n2p;
// 		_values[2] += ndays_n2p;
// 	}

// 	//@sk core reduce excessive day
// 	//@sk part1 reduce very large day to near-close range in one step
// 	int64_t nyears_p20 = _values[2] / 366;
// 	if (nyears_p20 > 0)
// 	{
// 		int64_t ndays_p20 = nyears_p20 * 365 + realtime::countLeap(_values[0], _values[0] + nyears_p20, _values[1] > 2 ? false : true, _values[1] > 2 ? true : false);
// 		_values[0] += nyears_p20;
// 		_values[2] -= ndays_p20;
// 	}

// 	//@sk part2 handle left months
// 	while (_values[2] > realtime::get_days_from_ym(_values[0], _values[1]))
// 	{
// 		_values[2] -= realtime::get_days_from_ym(_values[0], _values[1]);
// 		_values[1] += 1;
// 		if (_values[1] == 0)
// 		{
// 			_values[1] = 12;
// 			_values[0] -= 1;
// 			assert(_values[0] > 0);
// 		}
// 	}

// 	// sk ?? restore the fraud
// 	for (int i = myLevel + 1; i < 7; i++)
// 	{
// 		_values[i] = -1;
// 	}

// 	return;
// }

// int64_t realtime::years() const
// {
// 	return year();
// }

// int64_t realtime::months() const
// {
// 	return year() * 12 + month();
// }

// int64_t realtime::days() const
// {
// 	int64_t rst_days = day();
// 	// std::cout << seconds << std::endl;
// 	rst_days += ((year() - 1) * 365 + realtime::countLeap(1, year(), true, false));
// 	rst_days += (realtime::get_jdays(month(), 1, year()) - 1);
// 	return rst_days;
// }
// int64_t realtime::hours() const
// {
// 	return days() * 24 + hour();
// }
// int64_t realtime::minutes() const
// {
// 	return hours() * 60 + minute();
// }
// int64_t realtime::seconds() const
// {
// 	return minutes() * 60 + seconds();
// }
// int64_t realtime::mseconds() const
// {
// 	return -1;
// }

// int64_t realtime::stamp() const
// {
// 	switch (get_level())
// 	{
// 	case realevel::YEAR:
// 		return years();
// 		break;
// 	case realevel::MONTH:
// 		return months();
// 		break;
// 	case realevel::DAY:
// 		return days();
// 		break;
// 	case realevel::HOUR:
// 		return hours();
// 		break;
// 	case realevel::MINUTE:
// 		return minutes();
// 		break;
// 	case realevel::SECOND:
// 		return seconds();
// 		break;
// 	default:
// 		break;
// 	}
// 	return -1;
// }

// int64_t realtime::countLeap(long year1, long year2, bool with_left, bool with_right)
// {
// 	if (year1 > year2)
// 		return countLeap(year2, year1, with_right, with_left);
// 	auto countLeapFrom0 = [](long yr, bool with_boundary)
// 	{
// 		yr = abs(yr);
// 		return yr / 4 - yr / 100 + yr / 400 + (with_boundary ? 0 : -1) * realtime::isLeap(yr);
// 	};

// 	return countLeapFrom0(year2, with_right) * (year2 > 0 ? 1 : -1) - countLeapFrom0(year1, with_left) * (year1 > 0 ? 1 : -1);
// }

// int realtime::get_jdays(int month, int day, int year)
// {
// 	bool isLeap = realtime::isLeap(year);
// 	int jdays = 0;
// 	for (int i = 1; i < month; i++)
// 	{
// 		jdays += realtime::get_days_from_ym(year, i);
// 	}
// 	jdays += day;
// 	return jdays;
// }
// }