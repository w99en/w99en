#include <graphics.h>		// 引用 EasyX 图形库
#include <conio.h>
#define High 480  // 游戏画面尺寸
#define Width 640

//请在下方编写代码，完成一个圆类CCircle的定义，为其添加合适的属性和方法，其中属性包含圆移动的速度vx和vy，用于更新圆心坐标
class CCircle;

class CCircle {
	double x, y;
	double vx, vy;
	double r;
public:
	CCircle(double x1, double y1, double vx1, double vy1, double r1) : x(x1), y(y1), vx(vx1), vy(vy1), r(r1) {
	}
	void set(double x1, double y1) {
		x = x1;
		y = y1;

	}
	double getx() {
		return x;
	}
	double gety() {
		return y;
	}


	double getvx() {
		return vx;
	}
	double getvy() {
		return vy;
	}
	void ease() {
		setcolor(BLACK);
		setfillcolor(BLACK);
		fillcircle(x, y, r);
	}
	void redraw() {
		setcolor(YELLOW);
		setfillcolor(GREEN);
		fillcircle(x, y, r);
	}
	void change() {
		x = x + vx;
		y = y + vy;
	}
};


void updateWithoutInput(CCircle& obj) {
	obj.change();


}

void gameover() {
	EndBatchDraw();
	_getch();
	closegraph();
}

void startup() {
	initgraph(Width, High);//// 初始化640×480的画布
	BeginBatchDraw();
}


int main() {
	startup();

	//请在下方编写代码，生成一个CCircle类对象cobj
	CCircle cobj(2.0, 3.0, 1.0, 1.0,20.0);
	while (1) {
		cobj.ease();
		//请在下方编写代码，调用cobj的方法，擦除圆（就是用黑色把圆再画一遍）


		// 请在下方编写代码，调用updateWithoutInput函数，更新圆的坐标
		updateWithoutInput(cobj);

		//请在下方编写代码，调用cobj的方法，重新绘制圆

		cobj.redraw();

			FlushBatchDraw();
		// 延时
		Sleep(3);
	}



	gameover();
	return 0;
}