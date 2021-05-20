#ifndef TESTCALLURL_H
#define TESTCALLURL_H

#include "HttpOp.h"

class TestCallUrl : public QObject
{
    Q_OBJECT
public:

    explicit TestCallUrl();
    void test();
    void test2();

public slots:
   void loginFinish(QNetworkReply* );
};

#endif // TESTCALLURL_H
