#include "redtime.h"

#include<iostream>
using namespace redtime;

int main(){
	realtime real1(2014);
	realtimeseries rts2 = real1.rebase2rts(realevel::DAY);

	std::cout << rts2.data.size() << std::endl;
	std::cout << rts2.data[0].str() << std::endl;
	std::cout << rts2.data.back().str() << std::endl;

    return 0;
}
