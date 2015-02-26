#include <iostream>
#include <omp.h>
#include <time.h>
#include <math.h>
#include <string.h>
#include <vector>

int a[1000000], b[1000000];

//int main()
//{
	/*
	#pragma omp parallel num_threads(5)
	{
		std::cout << "Hello World!\n";
	}
	*/

	/*
	omp_set_num_threads(5);
#pragma omp parallel
	{
		std::cout << "Hello world!\n";
	}
	*/


	/*
	memset(a, 1, sizeof(int) * 1000000);
	memset(b, 1, sizeof(int) * 1000000);
#pragma omp parallel for
	for (int i = 1; i < 1000000 - 1; i++)
	{
		c[i] = a[i] * b[i] + a[i-1] *b[i+1];
	}
	*/

	/*
	int i, nthreads;
	clock_t clock_timer;
	double wall_timer;
	double c[1000000];

	for (nthreads = 1; nthreads <= 10; ++nthreads)
	{
		clock_timer = clock();
		wall_timer = omp_get_wtime();

#pragma omp parallel for private(i) num_threads(nthreads)
		for (i = 0; i < 1000000; i++)
		{
			c[i] = sqrt(i * 4 + i * 2 + i);
		}

		std::cout << "threads: " << nthreads << " time on clock(): " << (double) (clock() - clock_timer) / CLOCKS_PER_SEC << std::endl;

	}
	*/
//}


class omp_q 
{
	private:
		std::vector<int> queue;
		omp_lock_t lock;

	public:

		omp_q()
		{
			omp_init_lock(&lock);
		}
		~omp_q()
		{
			omp_destroy_lock(&lock);
		}

		bool push(const int& value)
		{
			omp_set_lock(&lock);
			queue.push_back(value);
			omp_unset_lock(&lock);
			return 1;
		}

};

int main()
{
	omp_q q;
	
	int i;
	clock_t clock_timer;

	clock_timer = clock();
#pragma omp parallel for private(i) num_threads(1)
	for (int i = 0; i < 1000000; i++ )
	{
		q.push(i);
	}

	std::cout << (double) clock() - clock_timer << std::endl;
	
}
















