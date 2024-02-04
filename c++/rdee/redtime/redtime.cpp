#include <stdexcept>
#include <iostream>
#include <climits>
#include <cassert>
#include "redtime.h"


namespace redtime {

	void time::sim_dhms()
	{
		//@sk core day-hour-minute-second part
		int64_t _seconds = seconds();
		if (_seconds >= 0)
		{
			day(_seconds / 86400);
		}
		else
		{
			day((_seconds - 86399) / 86400);
		}
		_seconds -= day() * 86400;
		hour(_seconds / 3600);
		_seconds -= hour() * 3600;
		minute(_seconds / 60);
		second(_seconds % 60);

		//@sk core year-month part
		//return *this;
	}


	int64_t time::seconds() const {
		return day() * 86400 + hour() * 3600 + minute() * 60 + second();
	}

	int64_t time::months() const {
		return year() * 12 + month();
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
		assert(year != 0 && month > 0 && month <= 12);
		const static int mdays[] = { 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };
		if (isLeap(year) && month == 2)
			return 29;
		else
			return mdays[month - 1]; //@sk hint Do not forget "-1"
	}

	itvtime& itvtime::operator+=(const itvtime& t2)
	{
		for (int i = 0; i < 7; i++)
			_values[i] += t2._values[i];
		return *this;
	}

	itvtime itvtime::operator+(const itvtime& t2) const
	{
		itvtime t6 = *this;
		t6 += t2;
		return t6;
	}

	itvtime& itvtime::operator-=(const itvtime& t2)
	{
		for (int i = 0; i < 7; i++)
			_values[i] -= t2._values[i];
		return *this;
	}

	itvtime itvtime::operator-(const itvtime& t2) const
	{
		itvtime t6 = *this;
		t6 -= t2;
		return t6;
	}


	itvtime& itvtime::add(const itvtime& t2)
	{
		*this += t2;
		return *this;
	}

	itvtime& itvtime::add(const itvtime* pt2)
	{
		*this += *pt2;
		return *this;
	}

	itvtime& itvtime::sub(const itvtime& t2)
	{
		*this -= t2;
		return *this;
	}

	itvtime& itvtime::sub(const itvtime* pt2)
	{
		*this -= *pt2;
		return *this;
	}

	void itvtime::sim() {
		sim_dhms();

		int64_t _months = months();
		if (_months < 0)
		{
			year((_months - 11) / 12);
		}
		else
		{
			year(_months / 12);
		}
		month(_months - year() * 12);
	}

	string itvtime::str() {
		return std::to_string(year()) + "/" + std::to_string(month()) + "/" + std::to_string(day()) + " " + std::to_string(hour()) + ":" + std::to_string(minute()) + ":" + std::to_string(second());
	}


	string realtime::str() {
		string rst = std::to_string(year());
		if (get_level() == realevel::YEAR)
			return rst;

		rst += ("/" + std::to_string(month()));
		if (get_level() == realevel::MONTH)
			return rst;

		rst += ("/" + std::to_string(day()));
		if (get_level() == realevel::DAY)
			return rst;

		rst += (" " + std::to_string(hour()));
		if (get_level() == realevel::HOUR)
			return rst;
		
		rst += (" " + std::to_string(minute()));
		if (get_level() == realevel::MINUTE)
			return rst;
		
		rst += (" " + std::to_string(second()));
		return rst;
	}

	realtime& realtime::operator+=(const itvtime& itv) {
		int myLevel = static_cast<int>(get_level());
		for (int i = 0; i < 7; i++)
			if (myLevel >= i)
				_values[i] += itv._values[i];
		//std::cout << str() << std::endl;
		sim();
		//std::cout << str() << std::endl;

		return *this;
	}

	realtime realtime::operator+(const itvtime& itv) const {
		realtime real2 = *this;
		real2 += itv;
		return real2;
	}

	realtime& realtime::operator-=(const itvtime& itv) {
		for (int i = 0; i < 7; i++)
			_values[i] -= itv._values[i];
		sim();

		return *this;
	}

	realtime realtime::operator-(const itvtime& itv) const {
		realtime real2 = *this;
		real2 -= itv;
		return real2;
	}

	//itvtime realtime::operator-(const realtime& real) const {
	//	realtime real2 = *this;
	//	real2 -= itv;
	//	return real2;
	//}


	void realtime::sim() {
		int myLevel = static_cast<int>(get_level());
		assert(get_level() != realevel::UNKNOWN);

		if (get_level() == realevel::YEAR)  //@sk exp branch only contain year, no need for simplification
			return;



		//sim_dhms();  //@sk exp simplify day-hour-minute-second first in uniform api

		//@sk core handel year-month logic separately
		int64_t _months = months();
		if (_months <= 0)
		{
			year((_months - 12) / 12);
		}
		else
		{
			year((_months - 1) / 12);
		}
		month(_months - year() * 12);
		assert(month() > 0 && month() < 13);

		if (get_level() == realevel::MONTH)
			return;
		//std::cout << str() << std::endl;


		//sk ?? make a fraud for convinence, need to be turned back after
		for (int i = myLevel + 1; i < 7; i++) {
			_values[i] = 0;
		}

		sim_dhms();

		//@sk core build a bridge between year-month and day
		if (_values[2] < 0) {  //@sk branch convert negative day to positive day, in yearly operation
			int64_t nyears_n2p = -_values[2] / 366 + 1;  //@sk exp years that makes day be positive
			int64_t ndays_n2p = nyears_n2p * 365 + realtime::countLeap(_values[0] - nyears_n2p, _values[0], _values[1] > 2 ? false : true, _values[1] > 2 ? true : false);
			_values[0] -= nyears_n2p;
			_values[2] += ndays_n2p;
		}

		//@sk core reduce excessive day
		//@sk part1 reduce very large day to near-close range in one step
		int64_t nyears_p20 = _values[2] / 366;
		if (nyears_p20 > 0) {
			int64_t ndays_p20 = nyears_p20 * 365 + realtime::countLeap(_values[0], _values[0] + nyears_p20, _values[1] > 2 ? false : true, _values[1] > 2 ? true : false);
			_values[0] += nyears_p20;
			_values[2] -= ndays_p20;
		}

		//@sk part2 handle left months
		while (_values[2] > realtime::get_days_from_ym(_values[0], _values[1])) {
			_values[2] -= realtime::get_days_from_ym(_values[0], _values[1]);
			_values[1] += 1;
			if (_values[1] == 0) {
				_values[1] = 12;
				_values[0] -= 1;
				assert(_values[0] > 0);
			}
		}

		//sk ?? restore the fraud
		for (int i = myLevel + 1; i < 7; i++) {
			_values[i] = -1;
		}

		return;
	}

	int64_t realtime::stamp() const
	{
		int64_t seconds;

		seconds = (day() - 1) * 86400 + hour() * 3600 + minute() * 60 + second();

		if (year() > 0)
		{
			// std::cout << seconds << std::endl;
			seconds += ((year() - 1) * 365 + realtime::countLeap(1, year(), false, false)) * 86400;
			seconds += (realtime::get_jdays(month(), 1, year()) - 1) * 86400;
		}
		else
		{
			throw std::logic_error("Not implemented for year < 0!");
			//seconds -= ((-year()) * 365 + realtime::countLeap(1, -year(), false, false)) * 86400;
			//seconds += (realtime::get_jdays(month(), 1, year()) - 1) * 86400;
		}
		return seconds;
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
}



//redtime redtime::operator+(const redtime &t2)
//{
//    redtime rt6 = t2;
//    rt6 += *this; //@sk exp 6, meme new
//    return rt6;
//}
//

//
//redtime redtime::operator-(const redtime &t2) const
//{
//    redtime rt6 = *this;
//    rt6 -= t2; //@sk exp 6, meme new
//    return rt6;
//}
//
//redtime &redtime::operator-=(const redtime &t2)
//{
//    if (!t2.isreal)
//    {
//        this->year -= t2.year;
//        this->month -= t2.month;
//        this->day -= t2.day;
//        this->hour -= t2.hour;
//        this->minute -= t2.minute;
//        this->second -= t2.second;
//        this->sim();
//    }
//    else if (!this->isreal && t2.isreal)
//    { //@sk branch exclude abs-real
//        throw std::runtime_error("Error! Cannot extract an abstime by a realtime");
//    }
//    else if (this->isreal && t2.isreal)
//    {
//        long stamp1 = this->stamp(), stamp2 = t2.stamp();
//        this->reset();
//        this->second = stamp2 - stamp1;
//        this->sim();
//        return *this;
//        if (this->isreal && !t2.isreal)
//        { //@sk branch rela-abs
//            this->real();
//        }
//        else
//        { //@sk branch for real-real, abs-abs
//            this->isreal = false;
//        }
//    }
//    return *this;
//}
//
//redtime &redtime::reset()
//{
//    this->year = 0;
//    this->month = 0;
//    this->day = 0;
//    this->hour = 0;
//    this->minute = 0;
//    this->second = 0;
//    this->isreal = false;
//
//    return *this;
//}
//
//redtime &redtime::sim()
//{
//    // std::cout << "enter sim" << std::endl;
//    long seconds = this->day * 86400 + this->hour * 3600 + this->minute * 60 + this->second;
//    if (seconds >= 0)
//    {
//        this->day = seconds / 86400;
//    }
//    else
//    {
//        this->day = (seconds - 86399) / 86400; // - 1;
//    }
//    seconds -= this->day * 86400;
//    this->hour = seconds / 3600;
//    seconds -= this->hour * 3600;
//    this->minute = seconds / 60;
//    this->second = seconds % 60;
//
//    // if (this->second < 0)
//    // {
//    //     this->minute -= -this->second / 60 + 1;
//    //     this->second = this->second % -60 + 50;
//    // }
//    // this->minute += this->second / 60;
//    // this->second %= 60;
//
//    // if (this->second < 0)
//    // {
//    //     this->minute -= -this->second / 60 + 1;
//    //     this->second = this->second % -60 + 50;
//    // }
//    // this->minute += this->second / 60;
//    // this->second %= 60;
//
//    // int carryHo = this->minute / 60;
//    // this->minute %= 60;
//    // this->hour += carryHo;
//    // int carryDa = this->hour / 24;
//    // this->hour %= 24;
//    // this->day += carryDa;
//
//    // std::cout << this->year << ' ' << this->month << ' ' << this->day << std::endl;
//
//    if (this->isreal)
//    {
//        int yrDays, moDays;
//        while (this->day > (yrDays = (isLeap(this->year) ? 366 : 365)))
//        {
//            this->day -= yrDays;
//            this->year += 1;
//        }
//        // std::cout << "cp1: " << this->year << ' ' << this->month << ' ' << this->day << std::endl;
//        while (this->day > (moDays = get_days_from_ym(this->year, this->month)))
//        {
//            // std::cout << "cp2: " << moDays << std::endl;
//            return *this;
//            this->day -= moDays;
//            // std::cout << this->year << ' ' << this->month << ' ' << this->day << std::endl;
//            this->nextMonth();
//            // this->month += 1;
//            // if (this->month > 12)
//            // {
//            //     this->year += 1;
//            //     this->month = 1;
//            // }
//        }
//    }
//    else
//    {
//        long months = this->year * 12 + this->month;
//        if (months < 0)
//        {
//            this->year = (months - 11) / 12; //  - (this->month % 12 == 0 ? 0 : 1);
//            // std::cout << months << ' ' << this->year;
//        }
//        else
//        {
//            this->year = months / 12;
//        }
//        this->month = months - this->year * 12;
//    }
//    return *this;
//}
//
//long redtime::stamp() const
//{
//    long seconds;
//
//    seconds = (this->day - 1) * 86400 + this->hour * 3600 + this->minute * 60 + this->second;
//
//    if (this->isreal)
//    {
//        if (this->year > 0)
//        {
//            // std::cout << seconds << std::endl;
//            seconds += ((this->year - 1) * 365 + redtime::countLeap(1, this->year, false, false)) * 86400;
//            seconds += (redtime::get_jdays(this->month, 1, this->year) - 1) * 86400;
//        }
//        else
//        {
//            seconds -= ((-this->year) * 365 + redtime::countLeap(1, -this->year, false, false)) * 86400;
//            seconds += (redtime::get_jdays(this->month, 1, this->year) - 1) * 86400;
//        }
//    }
//    return seconds;
//}
//
//redtime &redtime::real()
//{
//    if (this->year == 0)
//        this->year = 1;
//    if (this->month == 0)
//        this->month = 1;
//    if (this->day == 0)
//        this->day = 1;
//    this->isreal = true; //@sk exp set base to be 1-01-01 00:00:00
//    return *this;
//}
//
//int redtime::get_days_from_ym(int year, int month)
//{
//    // std::cout << year << month << std::endl;
//    assert(year != 0 && month > 0 && month <= 12);
//    int mdays[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
//    if (isLeap(year) && month == 2)
//        return 29;
//    else
//        return mdays[month - 1]; //@sk hint Do not forget "-1"
//}
//
//bool redtime::isLeap(int year)
//{
//    assert(year != 0);
//    if (year % 4 != 0)
//        return false;
//    else if (year % 100 != 0)
//        return true;
//    else if (year % 400 == 0)
//        return true;
//    else
//        return false;
//}
//
//redtime *redtime::realtime(int year, int month, int day, int hour, int minute, int second)
//{
//    redtime *p = new redtime(year, month, day, hour, minute, second);
//    p->isreal = true;
//    p->real();
//    return p;
//}
//
//redtime *redtime::abstime(int year, int month, int day, int hour, int minute, int second)
//{
//    redtime *p = new redtime(year, month, day, hour, minute, second);
//    p->isreal = false;
//    // p->realize();
//    return p;
//}
//
//
//redtime redtime::getDuration(const redtime &rt1, const redtime &rt2)
//{
//    if (rt1.isreal && rt2.isreal)
//    {
//        redtime rt6 = rt2 - rt1;
//        rt6.sim();
//        return rt6;
//    }
//    throw std::runtime_error("getDuration only works for two realtime");
//}
//
//redtime &redtime::lastMonth()
//{
//    assert(this->isreal);
//    redtime::lastMonth(this->year, this->month);
//    return *this;
//}
//
//redtime &redtime::nextMonth()
//{
//    assert(this->isreal);
//    redtime::nextMonth(this->year, this->month);
//    return *this;
//}
//
//void redtime::lastMonth(long &year, long &month)
//{
//    month -= 1;
//    if (month == 0)
//    {
//        year -= 1;
//        month = 12;
//        if (year == 0)
//            year = -1;
//    }
//}
//
//void redtime::nextMonth(long &year, long &month)
//{
//    // std::cout << "cp1: " << year << ' ' << month << std::endl;
//    month += 1;
//    if (month == 13)
//    {
//        year += 1;
//        month = 1;
//        if (year == 0)
//            year = 1;
//    }
//}
//

