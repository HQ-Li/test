#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QHBoxLayout>
#include <QDebug>
#include <QDateTime>
#include <QPushButton>
#include <QPixmap>
#include <QBitmap>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent)
    // ui(new Ui::MainWindow)
{
    treeWidget = new QTreeWidget();
    treeWidget->setHeaderHidden(true);
    treeWidget->setFixedWidth(200);

    connect(treeWidget, SIGNAL(itemClicked(QTreeWidgetItem *, int)), this, SLOT(treeItemClicked(QTreeWidgetItem*,int)));

    tableWidget = new QTableWidget();


    QHBoxLayout *hlayout = new QHBoxLayout();
    hlayout->addWidget(treeWidget);
    hlayout->addWidget(tableWidget);

    QWidget *widget  = new QWidget();

    loadData();

    // test
    {
        QPixmap pixmap("C:\\Users\\hqli\\OneDrive\\图片\\Snipaste_2022-03-03_11-33-09.png");
        QPushButton *toolBtn = new QPushButton;
        /*用于隐藏toolbutton的边框*/
        toolBtn->setStyleSheet("QToolButton{border:0px;}");
        /*调整按钮大小以适应图片的尺寸*/
        toolBtn->resize(pixmap.size());
        toolBtn->setIconSize(pixmap.size());
        toolBtn->setIcon(QIcon(pixmap));
        /*通过掩码设置按钮形状以适应图片的形状*/
        // toolBtn->setMask(pixmap.mask());
        hlayout->addWidget(toolBtn);
    }
    widget->setLayout(hlayout);
    this->setCentralWidget(widget);
}

void MainWindow::loadData()
{
    QTreeWidgetItem *project=new QTreeWidgetItem(treeWidget);
    project->setText(0, "project");

    QTreeWidgetItem *item11=new QTreeWidgetItem(project);
    item11->setText(0,"name1");

    QTreeWidgetItem *item2=new QTreeWidgetItem(project);
    item2->setText(0, "name2");
}

void MainWindow::loadProjectData()
{
    tableWidget->clear();
    tableWidget->setRowCount(10);
    tableWidget->setColumnCount(2);

    for (int i= 0; i < 10; i++) {
        tableWidget->setItem(i, 0, new QTableWidgetItem(QDateTime::currentDateTime().toString() + "sss"));
        tableWidget->setItem(i, 1, new QTableWidgetItem(QDateTime::currentDateTime().toString() + "ssaaa"));
    }

}

MainWindow::~MainWindow()
{
}

void MainWindow::treeItemClicked(QTreeWidgetItem* itme,int column)
{
    qDebug()<< __FUNCTION__ << itme->text(0) << column;
    loadProjectData();


}
