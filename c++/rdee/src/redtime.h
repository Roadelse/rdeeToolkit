#include <climits>

class redtime
{
public:
    int year;
    int month;
    int day;
    int hour;
    int minute;
    int second;
    redtime(int year = 0, int month = 0, int day = 0, int hour = 0, int minute = 0, int second = 0) : year(year), month(month), day(day), hour(hour), minute(minute), second(second){};
    redtime operator+(const redtime &t2);
    redtime &operator+=(const redtime &t2);
    redtime operator-(const redtime &t2);
    redtime &operator-=(const redtime &t2);

    // redtime operator*(const redtime &t2);
    redtime &realize();
    static int get_days_from_ym(int year, int month);
    static bool isLeap(int year);

    static redtime *realtime(int year = 0, int month = 0, int day = 0, int hour = 0, int minute = 0, int second = 0);

private:
    bool isreal = false;
};
