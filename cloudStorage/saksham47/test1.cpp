#include<bits/stdc++.h>

using namespace std;

int main()
{
	priority_queue<int> q;
	int n, T, k;
	int el;
	long long sum = 0;
	int max_el;
	int el1, el2;
	cin>>T;

	while(T--)
	{
		sum = 0;
		cin>>n>>k;

		for (int i = 0; i < n; ++i)
		{
			cin>>el;
			if (el > k)
				q.push(el);
			else
				sum+=el;
					/* code */
		}

		max_el = q.top();
		q.pop();

		while(q.size() > 1)
		{
			el1 = q.top();
			q.pop();

			el2 = q.top();
			q.pop();

			el1 -= (el2-k);
			sum += k;

			if (el1 > k)
				q.push(el1);
			else
				sum += el1;
		}

		if (q.size() == 1)
		{
			max_el -= (q.top() - k);
			sum += k + max_el;
		}

		else
			sum += max_el;	

		cout<<sum<<'\n';

	}
}