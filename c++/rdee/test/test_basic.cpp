#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include<stdexcept>
#include "headers/doctest.h"
#include "redtime.h"



TEST_CASE("testing redtime basic functionality, including +- operator") {
    redtime t1(2014, 01);
    redtime* abs1 = nullptr, * abs2 = redtime::abstime(0, 0, 1);
    abs1 = redtime::abstime(1, 2);
    redtime* real1 = nullptr, * real2 = redtime::realtime(2024, 2, 2, 11, 12, 34);
    real1 = redtime::realtime(2023, 4);

    CHECK(t1.year == 2014);
    CHECK(real1->day == 1);

    REQUIRE_THROWS_AS(*real1 + *real2, std::runtime_error);
    REQUIRE_THROWS_AS(*abs1 - *real2, std::runtime_error);

    redtime t2 = *real1 + *abs2;
    CHECK(t2.day == 2);
    *real2 -= *abs1;
    CHECK(real2->year == 2023); 
    CHECK(real2->month == 1);

    //@sk test method chaining
    CHECK(real1->add(abs1)->sub(real2)->year == 1);  //@K hint real2 has been altered above!
}

TEST_CASE("testing redtime::countLeap") {
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

TEST_CASE("testing redtime(...).stamp") {
    CHECK(redtime::realtime(1, 1, 1, 1, 1, 1)->stamp() == 3661);
    CHECK(redtime::realtime(-1, 12, 31, 0, 0, 0)->stamp() == -86400);
    CHECK(redtime::realtime(1970, 01, 01, 00, 00, 00)->stamp() == 62135596800);
    CHECK(redtime::realtime(2014, 12, 23, 23, 58, 34)->stamp() == 63554975914);
}
