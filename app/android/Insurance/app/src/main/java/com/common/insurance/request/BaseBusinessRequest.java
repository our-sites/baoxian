package com.common.insurance.request;

import android.text.TextUtils;

import com.alibaba.fastjson.JSON;
import com.common.insurance.net.EncrptResponseHandler;
import com.common.insurance.net.HttpClientManager;
import com.common.insurance.net.IRequest;
import com.common.insurance.net.IResponseHandler;
import com.common.insurance.net.InsuranceEncryptRequest;
import com.common.insurance.net.RequestError;

import org.json.JSONObject;

import java.util.Map;

/**
 * Created by wangyongchao on 16/10/19.
 */
public abstract class BaseBusinessRequest<T> {
    public static final int ACTION_SUCCESS = 0;

    public static final int ACTION_FAIL = 1;

    protected Map<String, String> mParams;//请求参数

    protected LoadCallback mCallback;//请求回调

    public BaseBusinessRequest() {
        this(null, null);
    }

    public BaseBusinessRequest(LoadCallback callback) {
        this(null, callback);
    }

    public BaseBusinessRequest(Map<String, String> params) {
        this(params, null);
    }

    public BaseBusinessRequest(Map<String, String> params,
                               LoadCallback callback) {
        this.mParams = params;
        this.mCallback = callback;
    }


    private IResponseHandler responseHandler = new EncrptResponseHandler() {
        @Override
        protected void onSuccess(IRequest request, JSONObject response) {

            T t = JSON.parseObject(response.toString(), getParseClass());
            if (mCallback != null) {
                mCallback.onLoadSuccess(t);
            }


        }

        @Override
        public void onFailure(IRequest request, RequestError error) {
            if (mCallback != null) {
                mCallback.onLoadFail(error);
            }

        }
    };

    protected Class<T> getParseClass() {
        return null;
    }


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
            request = new InsuranceEncryptRequest(getMethod(), urlPrefix + urlPostfix);
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
