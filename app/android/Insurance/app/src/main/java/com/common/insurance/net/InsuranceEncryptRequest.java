package com.common.insurance.net;

import android.content.Context;

public class InsuranceEncryptRequest extends AbsEncryptRequest {


    public InsuranceEncryptRequest(Context context, int method, String url) {
        super(context, method, url);
    }

    public InsuranceEncryptRequest(Context context, String url) {
        super(context, url);
    }


}
