#include<stdexcept>
#include<iostream>
#include <climits>
#include <cassert>
#include "redtime.h"

redtime redtime::operator+(const redtime& t2)
{
    redtime rt6 = t2;
    rt6 += *this;  //@sk exp 6, meme new
    return rt6;
}

redtime& redtime::operator+=(const redtime& t2)
{
    if (this->isreal && t2.isreal) {
        throw std::runtime_error("Error! Cannot add two realtime");
    }
    this->year += t2.year;
    this->month += t2.month;
    this->day += t2.day;
    this->hour += t2.hour;
    this->minute += t2.minute;
    this->second += t2.second;
    
    if (this->isreal || t2.isreal) {
        this->isreal = true;
        this->real();
    }
    return *this;
}

redtime redtime::operator-(const redtime& t2)
{
    redtime rt6 = *this;
    rt6 -= t2;  //@sk exp 6, meme new
    return rt6;
}

redtime& redtime::operator-=(const redtime& t2)
{
    if (!this->isreal && !t2.isreal) {
        this->year -= t2.year;
        this->month -= t2.month;
        this->day -= t2.day;
        this->hour -= t2.hour;
        this->minute -= t2.minute;
        this->second -= t2.second;
    }else if (!this->isreal && t2.isreal) {  //@sk branch exclude abs-real
        throw std::runtime_error("Error! Cannot extract an abstime by a realtime");
    }
    else if (this->isreal && t2.isreal) {

    }
    
    if (this->isreal && !t2.isreal) {  //@sk branch rela-abs
        this->real();
    }
    else {  //@sk branch for real-real, abs-abs
        this->isreal = false;
    }
    return *this;
}

redtime& redtime::sim() {
    if (this->isreal) {
        if (this->year == 0)
            this->year = 1;
        if (this->month == 0)
            this->month = 1;
        if (this->day == 0)
            this->day = 1;
    }

    int carryMi = this->second / 60;
    this->second %= 60;
    this->minute += carryMi;
    int carryHo = this->minute / 60;
    this->minute %= 60;
    this->hour += carryHo;
    int carryDa = this->hour % 24;
    this->hour %= 24;
    this->day += carryDa;

    int carryYr = this->month / 12;
    this->month %= 12;
    this->year += carryYr;

    if (this->isreal) {
        int yrDays, moDays;
        while (this->day > (yrDays = isLeap(this->year) ? 366 : 365))
        {
            this->day -= yrDays;
            this->year += 1;
        }
        while (this->day > (moDays = get_days_from_ym(this->year, this->month)))
        {
            this->day -= moDays;
            this->month += 1;
            if (this->month > 12)
            {
                this->year += 1;
                this->month = 1;
            }
        }
    }
    return *this;
}

long redtime::stamp() {
    long seconds;

    seconds = (this->day - 1) * 86400 + this->hour * 3600 + this->minute * 60 + this->second;

    if (this->isreal) {
        if (this->year > 0) {
            //std::cout << seconds << std::endl;
            seconds += ((this->year - 1) * 365 + redtime::countLeap(1, this->year, false, false)) * 86400;
            seconds += (redtime::get_jdays(this->month, 1, this->year) - 1) * 86400;
        }
        else {
            seconds -= ((-this->year) * 365 + redtime::countLeap(1, -this->year, false, false)) * 86400;
            seconds += (redtime::get_jdays(this->month, 1, this->year) - 1) * 86400;
        }
    }
    return seconds;
}

redtime& redtime::real()
{
    this->isreal = true;  //@sk exp set base to be 1-01-01 00:00:00
}

int redtime::get_days_from_ym(int year, int month)
{
    assert(year != 0 && month > 0 && month <= 12);
    int mdays[] = { 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };
    if (isLeap(year) && month == 2)
        return 29;
    else
        return mdays[month];
}

bool redtime::isLeap(int year)
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

redtime* redtime::realtime(int year, int month, int day, int hour, int minute, int second)
{
    redtime* p = new redtime(year, month, day, hour, minute, second);
    p->isreal = true;
    p->real();
    return p;
}

redtime* redtime::abstime(int year, int month, int day, int hour, int minute, int second)
{
    redtime* p = new redtime(year, month, day, hour, minute, second);
    p->isreal = false;
    //p->realize();
    return p;
}

redtime* redtime::add(const redtime& t2) {
    *this += t2;
    return this;
}

redtime* redtime::add(const redtime* pt2) {
    *this += *pt2;
    return this;
}

redtime* redtime::sub(const redtime& t2) {
    *this -= t2;
    return this;
}

redtime* redtime::sub(const redtime* pt2) {
    *this -= *pt2;
    return this;
}


redtime redtime::getDuration(const redtime & rt1, const redtime& rt2) {
    if (rt1.isreal && rt2.isreal) {
        redtime rt6 = rt2;
        rt6 -= rt1;
        rt6.sim();
        return rt6;
    }
}

redtime& redtime::lastMonth() {
    assert(this->isreal);
    redtime::lastMonth(this->year, this->month);
    return *this;
}

redtime& redtime::nextMonth() {
    assert(this->isreal);
    redtime::nextMonth(this->year, this->month);
    return *this;
}

void redtime::lastMonth(long& year, long& month) {
    month -= 1;
    if (month == 0) {
        year -= 1;
        month = 12;
        if (year == 0)
            year = -1;
    }
}

void redtime::nextMonth(long& year, long& month) {
    month += 1;
    if (month == 13) {
        year += 1;
        month = 1;
        if (year == 0)
            year = 1;
    }
}

long redtime::countLeap(long year1, long year2, bool with_left, bool with_right) {
    auto countLeapFrom0 = [](long yr, bool with_boundary) {
        yr = abs(yr);
        return yr / 4 - yr / 100 + yr / 400 + (with_boundary ? 0 : -1) * redtime::isLeap(yr);
    };

    return countLeapFrom0(year2, with_right) * (year2 > 0 ? 1 : -1) - countLeapFrom0(year1, with_left) * (year1 > 0 ? 1 : -1);
}

int redtime::get_jdays(int month, int day, int year) {
    bool isLeap = redtime::isLeap(year);
    int jdays = 0;
    for (int i = 1; i < month; i++) {
        jdays += redtime::get_days_from_ym(year, i);
    }
    jdays += day;
    return jdays;
}