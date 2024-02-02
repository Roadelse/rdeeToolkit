#pragma once

#include <climits>

class redtime
{
public:
    long year;
    long month;
    long day;
    long hour;
    long minute;
    long second;
    redtime(int year = 0, int month = 0, int day = 0, int hour = 0, int minute = 0, int second = 0) : year(year), month(month), day(day), hour(hour), minute(minute), second(second) {};

    redtime operator+(const redtime& t2);
    redtime& operator+=(const redtime& t2);
    redtime operator-(const redtime& t2);
    redtime& operator-=(const redtime& t2);

    redtime* add(const redtime& t2);
    redtime* add(const redtime *pt2);

    redtime* sub(const redtime& t2);
    redtime* sub(const redtime* pt2);
    // redtime operator*(const redtime &t2);
    redtime& sim();
    long stamp();
    redtime& real();
    static int get_days_from_ym(int year, int month);
    static bool isLeap(int year);

    redtime& lastMonth();
    redtime& nextMonth();

    static redtime* realtime(int year = 0, int month = 0, int day = 0, int hour = 0, int minute = 0, int second = 0);
    static redtime* abstime(int year = 0, int month = 0, int day = 0, int hour = 0, int minute = 0, int second = 0);

    static redtime getDuration(const redtime &rt1, const redtime & rt2);
    static void lastMonth(long &year, long &month);
    static void nextMonth(long &year, long &month);
    static long countLeap(long year1, long year2, bool leftOC = true, bool rightOC = true);
    static int get_jdays(int month, int day, int year = 1);
private:
    bool isreal = false;
};
