#include <graphics.h>		// 引用 EasyX 图形库
#include <conio.h>
#include<time.h>
#define High 480  // 游戏画面尺寸
#define Width 640

//请在下方编写代码，完成一个圆类CCircle的定义，为其添加合适的属性和方法
//请为圆类CCircle定义两个构造函数，不带参数的构造函数将生成大小、位置、速度均随机的圆（请保证在合理范围内随机）；
//带参数的构造函数将生成指定大小、位置和速度的圆。
class CCircle {
	double x, y;
	int r;
	double vx,vy;
public:
	CCircle(){
		srand(time(0));
		r = rand() % 50;
		x =( rand() % (640- r * 2) )+ r;
		y = (rand() % (480 - 2 * r) ) + r;
		vx = rand() % 20;
		vy = rand() % 20;
	}
	CCircle(double cx, double cy, int cr,double cvx,double cvy) {
		x = cx;
		y = cy;
		r = cr;
		vx = cvx;
		vy = cvy;
	}
	void picCircle() {
		setcolor(YELLOW);
		setfillcolor(GREEN);
		fillcircle(x, y, r);
	}
	void erCircle() {
		setcolor(BLACK);
		setfillcolor(BLACK);
		fillcircle(x, y, r);
	}
	void updateWithoutInput();

};

void CCircle::updateWithoutInput()
{
	
	if (x <= r || x >= Width - r)
		vx = -vx;
	if (y <= r || y >= High - r)
		vy = -vy;
	x = x + vx;
	y = y + vy;

}

void gameover()
{
	EndBatchDraw();
	_getch();
	closegraph();
}

void startup()
{
	initgraph(Width, High);//// 初始化640×480的画布
	BeginBatchDraw();
}


int main()
{
	startup();
	srand((unsigned int)time(0));

	//请在下方编写代码，生成一个指定大小、位置和速度的CCircle类对象cobj
	CCircle ccertain(50, 45, 30, 12, 12);

	//请在下方编写代码，生成一个大小、位置、速度均随机的CCircle类对象cobjrandom
	CCircle cobjrandom;


	while (1)
	{
		ccertain.erCircle();
		cobjrandom.erCircle();
		//请在下方编写代码，调用两个Circle对象方法，擦除圆（就是用黑色把圆再画一遍）
		ccertain.picCircle();
		cobjrandom.picCircle();
		ccertain.erCircle();
		cobjrandom.erCircle();



		// 请在下方编写代码，调用updateWithoutInput函数，更新两个Circle对象的坐标	
		ccertain.updateWithoutInput();
		cobjrandom.updateWithoutInput();



		//请在下方编写代码，调用两个Circle对象的方法，重新绘制圆

		ccertain.picCircle();
		cobjrandom.picCircle();



		FlushBatchDraw();
		Sleep(3);	// 延时
	}


	EndBatchDraw();
	closegraph();
	return 0;
}