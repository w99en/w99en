#include <graphics.h>		// 引用 EasyX 图形库
#include <conio.h>
#include<string>
#include<iostream>
#include<time.h>
using namespace std;

#define High 480  // 游戏画面尺寸
#define Width 640

//请在下方编写代码，完成一个圆类CCircle的定义，为其添加合适的属性和方法，其中属性包含圆移动的速度vx和vy，用于更新圆心坐标
class CCircle {
	int x, y, r;
	int vx, vy;
public:
	CCircle(int cx, int cy, int cr, int cvx, int cvy) {
		this->x = cx;
		this->y = cy;
		this->r = cr;
		this->vx = cvx;
		this->vy = cvy;
	}
	void set(int cx, int cy, int cr, int cvx, int cvy) {
		this->x = cx;
		this->y = cy;
		this->r = cr;
		this->vx = cvx;
		this->vy = cvy;
	}
	void updateWithoutInput(CCircle& obj);
	void ccircle() {
		
		setcolor(YELLOW);
		setfillcolor(GREEN);
		fillcircle(x, y, r);
	}
	void cobj() {
		setcolor(BLACK);
		setfillcolor(BLACK);
		fillcircle(x, y, r);
	}
	int meet_endge() {
		if ((x - r <= 0 || x + r >= Width) && (y - r <= 0 || y + r >= High))return 3;
		else if (y - r <= 0 || y + r >= High) return 2;
		else if (x - r <= 0 || x + r >= Width) return 1;
		else
			return 0;
	}
	void turn(CCircle& obj) {
		if (obj.meet_endge() == 3) {
			vy = -vy; vx = -vx;
		}
		else if (obj.meet_endge() == 2) vy = -vy;
		else vx = -vx;
	}
};


void CCircle::updateWithoutInput(CCircle& obj)
{
	obj.set(x + vx, y + vy, r, vx, vy);
	// 请在下方编写代码，调用obj的方法，更新圆的坐标

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

	//请在下方编写代码，生成一个CCircle类对象cobj
	srand(time(NULL));
	int r=rand()%40+10;
	int x = rand() % (640-2*r);
	int y = rand() % (480-2*r);
	CCircle c1(x, y, r, 5, 5);
	c1.ccircle();
	while (1)
	{
		if (c1.meet_endge())
			c1.turn(c1);
		//请在下方编写代码，调用cobj的方法，擦除圆（就是用黑色把圆再画一遍）
		c1.cobj();
		// 请在下方编写代码，调用updateWithoutInput函数，更新圆的坐标	
		c1.updateWithoutInput(c1);
		//请在下方编写代码，调用cobj的方法，重新绘制圆
		c1.ccircle();
		FlushBatchDraw();
		// 延时
		Sleep(3);
	}
	gameover();
	return 0;
}