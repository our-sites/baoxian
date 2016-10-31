package com.common.insurance.request;

import android.content.Context;
import android.content.Intent;
import android.os.Message;
import android.text.TextUtils;

import com.common.insurance.net.HttpClientManager;
import com.common.insurance.net.IRequest;
import com.common.insurance.net.IResponseHandler;
import com.common.insurance.net.InsuranceEncryptRequest;

import java.util.Map;

/**
 * Created by wangyongchao on 16/10/19.
 */
public abstract class BaseBusinessRequest {
    public static final int ACTION_SUCCESS = 0;

    public static final int ACTION_FAIL = 1;

    private final Context mContext;
    private final Message mMessage;
    protected Map<String, String> mParams;//请求参数

    public BaseBusinessRequest(Context context) {
        this(context, null, null);
    }

    public BaseBusinessRequest(Context context, Message message) {
        this(context, null, message);
    }

    public BaseBusinessRequest(Context context, Map<String, String> params) {
        this(context, params, null);
    }

    public BaseBusinessRequest(Context context, Map<String, String> params,
                               Message message) {
        this.mContext = context;
        this.mParams = params;
        this.mMessage = message;
    }

    private IResponseHandler responseHandler = new BaseBusinessResponseHandler() {
        @Override
        protected void onRequestSuccess(Object jsonObj) {

            BaseBusinessRequest.this.onSuccess(jsonObj);
        }

        @Override
        protected void onRequestFail() {

            BaseBusinessRequest.this.onFail();
        }

        @Override
        protected Object parseResponse(Object jsonObj) throws Exception {

            return BaseBusinessRequest.this.parseResponse(jsonObj);
        }
    };

    /**
     * 执行请求
     */
    public void execute() {
        HttpClientManager instance = HttpClientManager.getInstance();
        instance.execute(createRequest(), responseHandler);
    }

    private IRequest createRequest() {

        String urlPrefix = createRequestHostPrefix();

        String urlPostfix = createRequestHostPostfix();

        if (TextUtils.isEmpty(urlPrefix)) {
            urlPrefix = "";
        }

        if (TextUtils.isEmpty(urlPostfix)) {
            urlPostfix = "";
        }

        IRequest request = null;

        if (shouldEncry()) {
            request = new InsuranceEncryptRequest(mContext, getMethod(), urlPrefix + urlPostfix);
            ((InsuranceEncryptRequest) request).addParams(mParams);

        } else {

        }

        return request;
    }

    /**
     * 请求地址（前半部分）
     *
     * @return
     */
    protected abstract String createRequestHostPrefix();

    /**
     * 请求地址（后半部分）
     *
     * @return
     */
    protected abstract String createRequestHostPostfix();

    protected abstract Object parseResponse(Object data);

    public void onFail() {
        sendResponseMessage(ACTION_FAIL, "");
    }

    /**
     * 成功
     *
     * @param response
     */
    public void onSuccess(Object response) {
        sendResponseMessage(ACTION_SUCCESS, response);
    }

    private void sendResponseMessage(int result, Object response) {
        if (mMessage != null) {
            mMessage.arg1 = result;
            mMessage.obj = response;
            mMessage.sendToTarget();
        }
    }

    /**
     * 是否加密
     *
     * @return
     */
    protected boolean shouldEncry() {
        return true;
    }

    protected int getMethod() {
        return Method.POST;
    }

    /**
     * 目前仅支持Get和POST，后续有需求可以扩展
     */
    public interface Method {

        public static final int GET = 0;

        public static final int POST = 1;
    }
}
