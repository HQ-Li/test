#include "testcallurl.h"

#include <QObject>
#include <QJsonParseError>
#include <QJsonObject>
#include <QDebug>


TestCallUrl::TestCallUrl()
{

}

void TestCallUrl::test()
{
    HttpOp *loginHO = new HttpOp();

    QNetworkReply *reply;

    QByteArray byte_array;
    byte_array.append("password");
    QByteArray hash_byte_array = QCryptographicHash::hash(byte_array, QCryptographicHash::Md5);
    QString md5 = hash_byte_array.toHex();
    QString username = "error";

    QNetworkAccessManager *netWorkAccessManager = loginHO->url("http://music.163.com/api/login/")->data("username="+username+"&password="+md5+"&rememberLogin=true")
            ->mode(POST)->send(reply);

    QObject::connect(netWorkAccessManager, SIGNAL(finished(QNetworkReply*)), this, SLOT(loginFinish(QNetworkReply*)));
}

void TestCallUrl::loginFinish(QNetworkReply* reply)
{
    if (reply->error() == QNetworkReply::NoError)
    {
        // decode json string
        QJsonParseError jsonEr;
        QJsonObject jsonOb = QJsonObject(QJsonDocument::fromJson(reply->readAll(),&jsonEr).object());

        qDebug() << jsonOb;
    }
    else {
        qWarning(qPrintable(reply->errorString()));
    }
}


void TestCallUrl::test2()
{
    HttpOp *loginHO = new HttpOp();

    QNetworkReply *reply;

    QByteArray byte_array;
    byte_array.append("password");
    QByteArray hash_byte_array = QCryptographicHash::hash(byte_array, QCryptographicHash::Md5);
    QString md5 = hash_byte_array.toHex();
    QString username = "error";

    QByteArray allData = loginHO->url("http://music.163.com/api/login/")->data("username="+username+"&password="+md5+"&rememberLogin=true")
            ->mode(POST)->sendForSync(reply);

    QJsonParseError jsonEr;
    QJsonObject jsonOb = QJsonObject(QJsonDocument::fromJson(allData,&jsonEr).object());

    qDebug() << "all Data" << QString::fromUtf8(allData) ;
    qDebug() << "ssss:" << jsonOb.toVariantMap().value("msg").toString() ;


//    allData = loginHO->url("https://blog.csdn.net/weixin_42101997/article/details/84333986")->data("username="+username+"&password="+md5+"&rememberLogin=true")
//            ->mode(GET)->sendForSync(reply);

//    qDebug() << "all Data 2222" << QString::fromUtf8(allData) ;


}
