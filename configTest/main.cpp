#include "mainwindow.h"
#include <QApplication>
#include <QDebug>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();

    int *p = NULL;
    qDebug() << sizeof (double *) ;
    return a.exec();
}
