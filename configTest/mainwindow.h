#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTableWidget>
#include <QTreeWidget>


class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

public slots:
    void treeItemClicked(QTreeWidgetItem*,int);

private:
    void loadData();
    void loadProjectData();

    //Ui::MainWindow *ui;
    QTreeWidget *treeWidget;
    QTableWidget *tableWidget;


};

#endif // MAINWINDOW_H
