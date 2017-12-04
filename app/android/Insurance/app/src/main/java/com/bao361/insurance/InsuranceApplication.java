package com.bao361.insurance;

import android.app.Application;

import com.bao361.insurance.share.WXShareManager;
import com.bao361.insurance.utils.InsuranceConstans;
import com.tencent.mm.opensdk.openapi.IWXAPI;
import com.tencent.mm.opensdk.openapi.WXAPIFactory;

/**
 * Created by wangyongchao on 2017/8/31.
 */

public class InsuranceApplication extends Application {

    @Override
    public void onCreate() {
        super.onCreate();
        WXShareManager.getInstance().register(this);
    }

}
