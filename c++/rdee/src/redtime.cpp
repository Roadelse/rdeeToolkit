#include <climits>
#include <cassert>
#include "redtime.h"

redtime redtime::operator+(const redtime &t2)
{
    redtime rstTime(this->year + t2.year, this->month + t2.month, this->day + t2.day, this->hour + t2.hour, this->minute + t2.minute, this->second + t2.second);
    return rstTime;
}

redtime &redtime::operator+=(const redtime &t2)
{
    this->year += t2.year;
    this->month += t2.month;
    this->day += t2.day;
    this->hour += t2.hour;
    this->minute += t2.minute;
    this->second += t2.second;
    return *this;
}

redtime redtime::operator-(const redtime &t2)
{
    redtime rstTime(this->year - t2.year, this->month - t2.month, this->day - t2.day, this->hour - t2.hour, this->minute - t2.minute, this->second - t2.second);
    return rstTime;
}

redtime &redtime::operator-=(const redtime &t2)
{
    this->year -= t2.year;
    this->month -= t2.month;
    this->day -= t2.day;
    this->hour -= t2.hour;
    this->minute -= t2.minute;
    this->second -= t2.second;
    return *this;
}

redtime &redtime::realize()
{
    if (this->year == 0)
        this->year = 1;
    if (this->month == 0)
        this->month = 1;
    if (this->day == 0)
        this->day = 1;

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
    return *this;
}

int redtime::get_days_from_ym(int year, int month)
{
    assert(year != 0 && month > 0 && month <= 12);
    int mdays[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
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

redtime *redtime::realtime(int year, int month, int day, int hour, int minute, int second)
{
    redtime *p = new redtime(year, month, day, hour, minute, second);
    p->isreal = true;
    p->realize();
    return p;
}