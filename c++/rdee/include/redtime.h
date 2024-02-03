#pragma once

#include <cstdint>
#include <climits>
#include <cassert>

namespace redtime
{
    class time
    {
    public:
        time(int year = 0, int month = 0, int day = 0, int hour = 0, int minute = 0, int second = 0, int msecond = 0) : _values{year, month, day, minute, hour, second, msecond} {};

        int64_t year()
        {
            return _values[0];
        };
        int64_t month()
        {
            return _values[1];
        };
        int64_t day()
        {
            return _values[2];
        };
        int64_t hour()
        {
            return _values[3];
        };
        int64_t minute()
        {
            return _values[4];
        };
        int64_t second()
        {
            return _values[5];
        };
        int64_t msecond()
        {
            return _values[6];
        };
        virtual void year(int64_t val) const = 0;
        virtual void month(int64_t val) const = 0;
        virtual void day(int64_t val) const = 0;
        virtual void hour(int64_t val) const = 0;
        virtual void minute(int64_t val) const = 0;
        virtual void second(int64_t val) const = 0;
        virtual void msecond(int64_t val) const = 0;

    protected:
        int64_t _values[7];
    };

    class itvtime : public time
    {
    public:
        itvtime(int year = 0, int month = 0, int day = 0, int hour = 0, int minute = 0, int second = 0, int msecond = 0) : time(year, month, day, minute, hour, second, msecond){};
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
    };

    enum class realevel
    {
        UNKNOWN,
        YEAR,
        MONTH,
        DAY,
        HOUR,
        MINUTE,
        SECOND,
        MSECOND
    }

    class realtime : time
    {
    public:
        realtime(int year, int month = -1, int day = -1, int hour = -1, int minute = -1, int second = -1, int msecond = -1) : time(year, month, day, minute, hour, second, msecond){};

        realevel get_level()
        {
            if (rlevel != realevel::UNKNOWN)
                return rlevel;
            if
        }

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

    private:
        realevel rlevel = realevel::UNKNOWN;
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
//     static long countLeap(long year1, long year2, bool leftOC = true, bool rightOC = true);
//     static int get_jdays(int month, int day, int year = 1);

// private:
//     bool isreal = false;
// };
