#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include <stdexcept>
#include "headers/doctest.h"
#include "redtime.h"

using namespace redtime;

namespace Test_redtime
{
	TEST_CASE("randomTest") {

	}


	TEST_CASE("testing redtime definition")
	{
		itvtime itv1(1, 3, 5, 7, 9);
		realtime real1(2014, 01);
		CHECK(itv1.year() == 1);
		CHECK(real1.get_level() == realevel::MONTH);
	}

	TEST_CASE("testing itvtime::sim")
	{
		itvtime itv1(0, 0);
		itv1.sim();
		CHECK(itv1.year() == 0);
		CHECK(itv1.month() == 0);


		itvtime itv2(-1, -1);
		itv2.sim();
		CHECK(itv2.year() == -2);
		CHECK(itv2.month() == 11);


		itvtime itv3(-1, 24, 796, 61, 59, 61);
		itv3.sim();
		//std::cout << itv3.str() << std::endl;
		CHECK(itv3.year() == 1);
		CHECK(itv3.month() == 0);
		CHECK(itv3.day() == 798);
		CHECK(itv3.hour() == 14);
		CHECK(itv3.minute() == 0);
		CHECK(itv3.second() == 1);


		itvtime itv4(0, -12, 1, -1, 1, -3661);
		itv4.sim();
		CHECK(itv4.year() == -1);
		CHECK(itv4.month() == 0);
		CHECK(itv4.second() == 59);
		CHECK(itv4.minute() == 59);
		CHECK(itv4.hour() == 21);
		CHECK(itv4.day() == 0);
		CHECK(itv4.months() == -12);
		CHECK(itv4.seconds() == 79199);
	}

	TEST_CASE("testing realtime base +-")
	{
		realtime real1(2024, 2, 4, 14, 45, 59);
		real1.sim();
		REQUIRE(real1.str() == "2024/2/4 14:45:59");
			
		REQUIRE_THROWS(realtime(2024, 2, 4, 14, 45, 60));

		realtime real2 = real1 + itvtime(0,-20);
		REQUIRE(real2.str() == "2022/6/4 14:45:59");

		realtime real3 = real1 + itvtime(-1, 0, 25, 0, -1, 1);
		REQUIRE(real3.str() == "2023/3/1 14:45:0");
		realtime real3B = real1 + itvtime(0, 0, 25, 0, -1, 1);
		REQUIRE(real3B.str() == "2024/2/29 14:45:0");

		realtime real4 = real1 + itvtime(0, 0, 0, 1234, 5678, 9101112);
		REQUIRE(real4.str() == "2024/7/14 7:29:11");

		realtime real5 = real1 + itvtime(0, 0, -1234 , -5678, -9101112, -13141516);
		REQUIRE(real5.str() == "2002/5/7 17:8:43");

		realtime real5B = real1 - itvtime(0, 0, 1234, 5678, 9101112, 13141516);
		REQUIRE(real5B.str() == "2002/5/7 17:8:43");

	}

	TEST_CASE("testing realtime scale +-") {
		realtime real1(2024);

		//@sk exp test invalid month
		realtime real2 = real1 + itvtime(-1, 300);
		REQUIRE(real2.str() == "2023");

		//@sk test invalid minute
		realtime real3 = realtime(2024, 2, 4, 0, 1) - itvtime(0, 0, 0, 0, 0, 3600);
		REQUIRE(real2.str() == "2024/2/4 0:1");

	}


	TEST_CASE("testing realtime::countLeap")
	{
		CHECK(realtime::countLeap(1, 1) == 0);
		CHECK(realtime::countLeap(1, 100) == 24);
		CHECK(realtime::countLeap(100, 104) == 1);
		CHECK(realtime::countLeap(-104, -100) == 1);
		CHECK(realtime::countLeap(-100, 100) == 48);
		CHECK(realtime::countLeap(1, 400) == 97);
		CHECK(realtime::countLeap(-400, 100) == 121);
		CHECK(realtime::countLeap(-100, 400) == 121);
		CHECK(realtime::countLeap(-104, 400) == 122);
		CHECK(realtime::countLeap(-104, 400, false) == 121);
		CHECK(realtime::countLeap(-104, 402) == 122);
		CHECK(realtime::countLeap(-105, 401, false, false) == 122);
	}

	TEST_CASE("testing realtime::stamp")
	{
		CHECK(realtime(1, 1, 1, 1, 1, 1).stamp() == 3661);
		REQUIRE_THROWS(realtime(-1, 12, 31, 0, 0, 0).stamp());
		CHECK(realtime(1970, 01, 01, 00, 00, 00).stamp() == 62135596800);
		CHECK(realtime(2014, 12, 23, 23, 58, 34).stamp() == 63554975914);
	}
}