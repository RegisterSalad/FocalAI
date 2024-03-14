#include "mainwindow.h"
#include "./ui_mainwindow.h"
#include <cstdlib>
//#include "Python.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    // Connect the QPushButton's clicked signal to the runCustomPythonScript slot
    connect(ui->pushButton, &QPushButton::clicked, this, &MainWindow::on_pushButton_clicked);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_verticalWidget_2_customContextMenuRequested(const QPoint &pos)
{

}


void MainWindow::on_pushButton_clicked()
{
    /*
    // Initialize the Python interpreter
    Py_Initialize();

    // Specify the name of your custom Python script
    const char* customScriptName = "MyMainWindow.py";

    // Build the command to execute the Python script
    std::string command = std::string("python ") + customScriptName;

    // Execute the command using std::system
    int result = std::system(command.c_str());

    // Check the result if needed
    if (result == 0) {
        qDebug() << "Custom Python script executed successfully.";
    } else {
        qDebug() << "Error executing Custom Python script.";
    }

    // Finalize the Python interpreter
    Py_Finalize();
*/
}

