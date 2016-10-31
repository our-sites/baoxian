package com.common.insurance.net;

import android.content.Context;

import com.common.insurance.utils.InsuranceLogger;
import com.common.insurance.utils.InsuranceUtils;
import com.common.insurance.utils.JsonUtil;
import com.common.insurance.utils.StringUtil;

import org.json.JSONObject;

import java.util.HashMap;
import java.util.IdentityHashMap;
import java.util.Map;

public abstract class AbsEncryptRequest implements IRequest {

    protected Context mContext;
    protected int mMethod;
    protected String mUrl;

    private static final String ENCRYPT_PARAMS_KEY = "edata";

    private Map<String, String> mParams;

    private boolean mShouldGZIP = false;//是否需要压缩


    public AbsEncryptRequest(Context context, int method, String url) {
        this.mContext = context;
        this.mMethod = method;
        this.mUrl = url;

    }

    public AbsEncryptRequest(Context context, String url) {
        this(context, Method.POST, url);
    }


    @Override
    public String getUrl() {
        return mUrl;
    }

    @Override
    public void setUrl(String url) {
        this.mUrl = url;
    }

    @Override
    public Map<String, String> getRequestParmas() {

        Map<String, String> params = new HashMap<String, String>();

        // 对于公共头和普通参数转化为JsonObject
        JSONObject jsonObj = new JSONObject();

        try {
            long timestamp = System.currentTimeMillis();
            // 追加标准header头
            jsonObj.put("header",
                    JsonUtil.parseMap2JsonObject(InsuranceUtils.getCommonHeader()));

            JSONObject bodyJson = JsonUtil.parseMap2JsonObject(mParams);
            bodyJson.put("proxy_timestamp", timestamp);

            jsonObj.put("body", bodyJson);

            String edata = jsonObj.toString();

            InsuranceLogger.d("net",edata);

            //预留对数据进行加密，压缩
            String encryptedData = gzipOrEncryptPostData(edata);

            params.put(ENCRYPT_PARAMS_KEY, edata);

            // 增加CRC校验参数
            params.put("crc", StringUtil.md5(edata));


        } catch (Exception e) {

        }
        return params;
    }

    @Override
    public Map<String, String> getOrginalParmas() {

        return mParams;
    }

    public void addParam(String key, String value) {

        if (mParams == null) {
            mParams = new IdentityHashMap<String, String>();
        }

        mParams.put(key, value);

    }

    public void addParams(Map<String, String> params) {

        if (mParams == null) {
            mParams = new IdentityHashMap<String, String>();
        }

        if (params == null || params.size() == 0) {
            return;
        }

        mParams.putAll(params);

    }

    private String gzipOrEncryptPostData(String postData) throws Exception {

        if (postData == null) {
            return null;
        }

        byte[] data = postData.getBytes();

        if (shouldGZIP()) {
            data = StringUtil.compressToByte(data);
        }

        if (shouldEncrypt()) {
//            return encryptPostData(data);执行加密数据
        }

        return postData;
    }

    private boolean shouldEncrypt() {
        return false;
    }

    public boolean shouldGZIP() {
        return mShouldGZIP;
    }

    @Override
    public int getMethod() {
        return mMethod;
    }
}
