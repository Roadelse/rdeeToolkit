#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include <stdexcept>
#include "doctest/doctest.h"
#include "redtime.h"

using namespace redtime;

namespace Test_redtime
{
	TEST_CASE("randomTest")
	{
		// realtime real1(2014);
		// std::vector<realtime> list;
		// list.push_back(real1);
		// list.push_back(real1);
		// std::cout << real1.str() << std::endl;
		// std::cout << list[0].str() << std::endl;
		// std::cout << list.back().str() << std::endl;

		realtime real1(2014, 12, 31);
		real1 += freetime(0, 0, 1);
	}

	TEST_CASE("testing redtime definition")
	{
		freetime itv1(1, 3, 5, 7, 9);
		// realtime real1(2014, 01);
		CHECK(itv1.year() == 1);
		// CHECK(real1.get_level() == realevel::MONTH);
	}

	TEST_CASE("testing freetime::sim")
	{
		freetime frt1(0, 0);
		frt1.sim();
		CHECK(frt1.year() == 0);
		CHECK(frt1.month() == 0);

		freetime itv2(-1, -1);
		itv2.sim();
		REQUIRE(itv2.str() == "-2/11/0 0:0:0");

		freetime itv3(-1, 24, 796, 61, 59, 61);
		itv3.sim();
		REQUIRE(itv3.str() == "1/0/798 14:0:1");

		freetime itv4(0, -12, 1, -1, 1, -3661);
		itv4.sim();
		REQUIRE(itv4.str() == "-1/0/0 21:59:59");
	}

	TEST_CASE("testing freetime::count")
	{
		freetime frt1(-1, -1, -1, -1, -1, -1);
		REQUIRE(frt1.months() == -13);
		REQUIRE(frt1.years() == -2);
		REQUIRE(frt1.days() == -2);
		REQUIRE(frt1.hours() == -26);
		REQUIRE(frt1.str() == "-1/-1/-1 -1:-1:-1");
		frt1.sim();
		REQUIRE(frt1.str() == "-2/11/-2 22:58:59");
	}

	TEST_CASE("testing freetime::+-")
	{
		freetime frt1 = freetime(-1, 1, -1, 1, -1, 1) + freetime(1, -1, 1, -1, 1, -1);
		REQUIRE(frt1.str() == "0/0/0 0:0:0");
		REQUIRE(frt1.add(freetime(1, 1, 1, 2, 2, 2)).str() == "1/1/1 2:2:2");
		REQUIRE(frt1.sub(freetime(2, 1, 1, 1, 1, 1)).str() == "-1/0/0 1:1:1");
	}

	TEST_CASE("testing realtime base")
	{
		realtime real1 = realtime(2024, 2, 5, 11, 4, 59);
		REQUIRE(real1.get_timescale() == realevel::SECOND);
		realtime real2 = realtime(2024, 2, 5);
		REQUIRE(real2.get_timescale() == realevel::DAY);
		REQUIRE(real2.hour(11).get_timescale() == realevel::HOUR);
		REQUIRE_THROWS(real2.second(58));
		realtime real3(2024);

		// REQUIRE(real3.get_timescale() == realevel::YEAR);
		// REQUIRE(real3.str() == "2024");

		// realtime real3X = real3.month(2).day(28).hour(11).minute(58);
		// REQUIRE(real3X.str() == "2024/2/28 11:58");
	}

	TEST_CASE("testing realtime base +-")
	{
		realtime real1(2024, 2, 4, 14, 45, 59);
		real1.sim();
		REQUIRE(real1.str() == "2024/2/4 14:45:59");

		REQUIRE_THROWS(realtime(2024, 2, 4, 14, 45, 60));

		realtime real2 = real1 + freetime(0, -20);
		REQUIRE(real2.str() == "2022/6/4 14:45:59");

		realtime real3 = real1 + freetime(-1, 0, 25, 0, -1, 1);
		REQUIRE(real3.str() == "2023/3/1 14:45:0");
		realtime real3B = real1 + freetime(0, 0, 25, 0, -1, 1);
		REQUIRE(real3B.str() == "2024/2/29 14:45:0");

		realtime real4 = real1 + freetime(0, 0, 0, 1234, 5678, 9101112);
		REQUIRE(real4.str() == "2024/7/14 7:29:11");

		realtime real5 = freetime(0, 0, -1234, -5678, -9101112, -13141516) + real1; //@sk exp test freetime + realtime
		REQUIRE(real5.str() == "2002/5/7 17:8:43");

		realtime real5B = real1 - freetime(0, 0, 1234, 5678, 9101112, 13141516);
		REQUIRE(real5B.str() == "2002/5/7 17:8:43");

		freetime frt1 = real1 - realtime(2024, 2, 4, 14, 46, 0);
		REQUIRE(frt1.str() == "0/0/0 0:0:-1");
		REQUIRE_THROWS(real1 - realtime(2024, 2, 4, 14, 46));

		freetime frt2 = realtime(2024, 2, 4) - realtime(2023, 2, 4);
		REQUIRE(frt2.str() == "0/0/365 0:0:0");
	}

	TEST_CASE("testing realtime scale +-")
	{
		realtime real1(2024);

		//@sk exp test invalid month
		realtime real2 = real1 + freetime(-1, 300);
		REQUIRE(real2.str() == "2023");
        REQUIRE(real2.month() == -1);

		//@sk test invalid minute
		realtime real3 = realtime(2024, 2, 4, 0, 1) - freetime(0, 0, 0, 0, 0, 3600);
		REQUIRE(real3.str() == "2024/2/4 0:1");
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

		CHECK(realtime(2014).stamp() == 2014);
		CHECK(realtime(3, 12).stamp() == 36);
		CHECK(realtime(3, 12, 4).stamp() == 1068);
		CHECK(realtime(3, 12, 4, 10).stamp() == 1067 * 24 + 10);
	}

	TEST_CASE("testing realtime::rebase") {
		realtime real1(2014);
		realtime real2 = real1.rebase(realevel::MONTH);
		REQUIRE(real2.get_timescale() == realevel::MONTH);
		REQUIRE(real2.str() == "2014/1");
		realtime real3 = real2.rebase(realevel::HOUR);
		REQUIRE(real3.get_timescale() == realevel::HOUR);
		REQUIRE(real3.str() == "2014/1/1 0");

		realtimeseries rts1 = real1.rebase2rts(realevel::MONTH);
		REQUIRE(rts1.data.size() == 12);
		REQUIRE(rts1.get_timescale() == realevel::MONTH);
		REQUIRE(rts1.data.front().str() == "2014/1");
		REQUIRE(rts1.data[5].str() == "2014/6");
		REQUIRE(rts1.data.back().str() == "2014/12");

		realtimeseries rts2 = real1.rebase2rts(realevel::HOUR);
		REQUIRE(rts2.data.size() == 8760);
		REQUIRE(rts2.get_timescale() == realevel::HOUR);
		REQUIRE(rts2.data.front().str() == "2014/1/1 0");
		REQUIRE(rts2.data.back().str() == "2014/12/31 23");

		realtime real4(2024, 2, 6);
		realtimeseries rts3 = real4.rebase2rts(realevel::SECOND);
		REQUIRE(rts3.data.size() == 86400);
		REQUIRE(rts3.get_timescale() == realevel::SECOND);
		REQUIRE(rts3.data.front().str() == "2024/2/6 0:0:0");
		REQUIRE(rts3.data.back().str() == "2024/2/6 23:59:59");
	}

	TEST_CASE("testing realtimeseries::rebase") {
		realtimeseries rts1(realtime(2014), realtime(2024), freetime(1));
		realtimeseries rts1_rb = rts1.rebase(realevel::MONTH);
		REQUIRE(rts1_rb.data.size() == 132);

		realtimeseries rts1_rb2 = rts1.rebase(realevel::DAY);
		REQUIRE(rts1_rb2.data.size() == 4018);
		REQUIRE(rts1_rb2.data.front().str() == "2014/1/1");
		REQUIRE(rts1_rb2.data.back().str() == "2024/12/31");

	}


	TEST_CASE("testing realtimeseries")
	{
		realtimeseries rts1(realtime(2014), realtime(2024), freetime(1));
		REQUIRE(rts1.data.size() == 11);
		REQUIRE(rts1.data[0].str() == "2014");
		REQUIRE(rts1.data[10].str() == "2024");
		REQUIRE(rts1.data[9].str() == "2023");

		REQUIRE_THROWS(realtimeseries(realtime(2014), realtime(2024), freetime(0, 1)));

		realtimeseries rts2 = realtimeseries(realtime(2024, 01, 01), realtime(2024, 12, 31), freetime(0, 0, 1));
		REQUIRE(rts2.data.size() == 366);
		REQUIRE(rts2.data[0].str() == "2024/1/1");
		REQUIRE(rts2.data[59].str() == "2024/2/29");
		REQUIRE(rts2.data.back().str() == "2024/12/31");
	}

}
