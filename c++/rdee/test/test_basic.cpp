#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include <stdexcept>
#include "headers/doctest.h"
#include "redtime.h"

namespace Test_redtime
{
    TEST_CASE("testing redtime definition")
    {
        std::cout << "-13 % -12 = " << -13 % -12 << std::endl;
        redtime t1(2014, 01);
        redtime *abs1 = nullptr, *abs2 = redtime::abstime(0, 0, 1);
        abs1 = redtime::abstime(1, 2);
        redtime *real1 = nullptr, *real2 = redtime::realtime(2024, 2, 2, 11, 12, 34);
        real1 = redtime::realtime(2023, 4);

        CHECK(t1.year == 2014);
        CHECK(real1->day == 1);
    }

    TEST_CASE("testing sim")
    {
        // redtime *abs1 = redtime::abstime(0, 0);
        // abs1->sim();
        // CHECK(abs1->year == 0);
        // CHECK(abs1->month == 0);

        // redtime *abs2 = redtime::abstime(-1, -1);
        // abs2->sim();
        // CHECK(abs2->year == -2);
        // CHECK(abs2->month == 11);

        // redtime *abs3 = redtime::abstime(-1, 24, 796, 61, 59, 61);
        // abs3->sim();
        // CHECK(abs3->year == 1);
        // CHECK(abs3->month == 0);
        // CHECK(abs3->day == 798);
        // CHECK(abs3->hour == 14);
        // CHECK(abs3->minute == 0);
        // CHECK(abs3->second == 1);

        // redtime *abs4 = redtime::abstime(0, -12, 1, -1, 1, -3661);
        // abs4->sim();
        // CHECK(abs4->year == -1);
        // CHECK(abs4->month == 0);
        // CHECK(abs4->second == 59);
        // CHECK(abs4->minute == 59);
        // CHECK(abs4->hour == 21);
        // CHECK(abs4->day == 0);

        redtime *real1 = redtime::realtime();
        CHECK(real1->year == 1);
        CHECK(real1->month == 1);
        CHECK(real1->day == 1);

        // redtime *real1 = redtime::realtime(2014, -24, 90, 380, -1723, 9876);
        // real1->sim();
        // CHECK(real1->year == 2012);
        // CHECK(real1->month == 0);
        // CHECK(real1->second == 59);
        // CHECK(real1->minute == 59);
        // CHECK(real1->hour == 21);
        // CHECK(real1->day == 0);
    }
    // REQUIRE_THROWS_AS(*real1 + *real2, std::runtime_error);
    // REQUIRE_THROWS_AS(*abs1 - *real2, std::runtime_error);

    // redtime t2 = *real1 + *abs2;
    // CHECK(t2.day == 2);
    // *real2 -= *abs1;
    // CHECK(real2->year == 2022);
    // CHECK(real2->month == 12);

    // //@sk test method chaining
    // CHECK(real1->add(abs1)->sub(real2)->year == 1); //@K hint real2 has been altered above!

    TEST_CASE("testing redtime::countLeap")
    {
        CHECK(redtime::countLeap(1, 1) == 0);
        CHECK(redtime::countLeap(1, 100) == 24);
        CHECK(redtime::countLeap(100, 104) == 1);
        CHECK(redtime::countLeap(-104, -100) == 1);
        CHECK(redtime::countLeap(-100, 100) == 48);
        CHECK(redtime::countLeap(1, 400) == 97);
        CHECK(redtime::countLeap(-400, 100) == 121);
        CHECK(redtime::countLeap(-100, 400) == 121);
        CHECK(redtime::countLeap(-104, 400) == 122);
        CHECK(redtime::countLeap(-104, 400, false) == 121);
        CHECK(redtime::countLeap(-104, 402) == 122);
        CHECK(redtime::countLeap(-105, 401, false, false) == 122);
    }

    TEST_CASE("testing redtime(...).stamp")
    {
        CHECK(redtime::realtime(1, 1, 1, 1, 1, 1)->stamp() == 3661);
        CHECK(redtime::realtime(-1, 12, 31, 0, 0, 0)->stamp() == -86400);
        CHECK(redtime::realtime(1970, 01, 01, 00, 00, 00)->stamp() == 62135596800);
        CHECK(redtime::realtime(2014, 12, 23, 23, 58, 34)->stamp() == 63554975914);
    }
}