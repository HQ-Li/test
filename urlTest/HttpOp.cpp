#include "httpop.h"
#include <QEventLoop>

// set send data for class member
HttpOp* HttpOp::data(QString sdata)
{
    this->mdata = sdata;
    this->mQdataArray.append(sdata);
    this->mNetRequest.setHeader(QNetworkRequest::ContentLengthHeader, this->mQdataArray.length());
    return this;
}

// set send mode (post or get)
HttpOp* HttpOp::mode(QString smode)
{
    this->mmode = smode;
    return this;
}

void HttpOp::init()
{
    mNetManager = new QNetworkAccessManager();
    //this->mNetRequest.setRawHeader("Accept","*/*");
    //this->mNetRequest.setRawHeader("Accept-Language","zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4");
    //this->mNetRequest.setRawHeader("Connection","keep-alive");
    //this->mNetRequest.setRawHeader("Host","music.163.com");
    this->mNetRequest.setRawHeader("Referer","http://music.163.com/search/");
    this->mNetRequest.setHeader(QNetworkRequest::UserAgentHeader,"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36");
    this->mNetRequest.setHeader(QNetworkRequest::ContentTypeHeader, "application/x-www-form-urlencoded");
    //this->mNetRequest.setHeader(QNetworkRequest::CookieHeader,"appver=1.5.2");
}

HttpOp* HttpOp::url(QString surl)
{
    this->mUrl = surl;
    this->mNetRequest.setUrl(QUrl(surl));
    return this;
}

// Structure function
HttpOp::HttpOp()
{
    this->mode(GET);
    this->init();
}



HttpOp::~HttpOp()
{
    delete this->mNetManager;
}

QByteArray HttpOp::sendForSync(QNetworkReply* &reply)
{
    if(this->mmode == POST) reply = mNetManager->post(this->mNetRequest,this->mQdataArray);
    else{
        this->mNetRequest.setUrl(QUrl(QString(this->mUrl)));
        reply = mNetManager->get(this->mNetRequest);
    }

    QEventLoop eventLoop;
    QObject::connect(reply, SIGNAL(finished()), &eventLoop, SLOT(quit()));
    eventLoop.exec();

    if (reply->error() == QNetworkReply::NoError) {
        int totlalLength = reply->rawHeader("Content-Length").toInt();
        int reciveLength = 0;

        while (true)
        {
            QByteArray byteArray = reply->readAll();
            QString rlt = QString::fromUtf8(byteArray);
            qDebug() << "rlt###:" << rlt;

            reciveLength += byteArray.count();


            bool isFinish = reply->isFinished();
            qDebug() << "isFinish#:" << isFinish;

            if (reply->isFinished())
            {
                qDebug() << QStringLiteral("下载数据完成的。");
                return byteArray;
            }
            if (totlalLength == reciveLength)
            {
                qDebug() << "length == reciveLength:";
                qDebug() << QStringLiteral("下载数据完成的。");
                return byteArray;
            }

        }
        //reply->deleteLater();
    }
    else {
        qWarning() << "request "<< mUrl << " error: " << reply->error();
    }
}

// send data
QNetworkAccessManager* HttpOp::send(QNetworkReply* &reply)
{
    if(this->mmode == POST) reply = mNetManager->post(this->mNetRequest,this->mQdataArray);
    else{
        this->mNetRequest.setUrl(QUrl(QString(this->mUrl)));
        reply = mNetManager->get(this->mNetRequest);
    }
    return mNetManager;
}
