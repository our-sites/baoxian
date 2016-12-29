package com.common.insurance.net;

import android.util.Log;

import com.common.insurance.utils.InsuranceLogger;

import java.io.IOException;
import java.io.InputStream;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.TimeUnit;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

/**
 * Created by wangyongchao on 16/10/18.
 * 管理okhttpclient
 */
public class HttpClientManager<T> {
    private static HttpClientManager mInstance = null;
    private OkHttpClient mOkHttpClient;
    private OkHttpClient.Builder builder;

    private HttpClientManager() {
        initOkHttpBuilder();
        mOkHttpClient = builder.build();
    }


    private void initOkHttpBuilder() {
        builder = new OkHttpClient.Builder();
        builder.connectTimeout(15, TimeUnit.SECONDS); //连接超时15毫秒
    }

    public static synchronized HttpClientManager getInstance() {

        if (mInstance == null) {
            mInstance = new HttpClientManager();
        }
        return mInstance;
    }

    public OkHttpClient.Builder getBuilder() {
        return builder;
    }

    public OkHttpClient getOkHttpClient() {
        return mOkHttpClient;
    }


    public void execute(IRequest request, IResponseHandler responseHandler) {

        int method = request.getMethod();
        if (method == IRequest.Method.POST) {//post请求
            requestByPost(request, responseHandler);

        } else if (method == IRequest.Method.GET) {//get请求
            requestByGet(request, responseHandler);
        }


    }

    /**
     * post请求
     * 请求体 ip=58.215.185.154&dtype=json&format=&key=177038539bb5e9c91c8a1443145d3765"
     */
    private void requestByPost(final IRequest request, final IResponseHandler responseHandler) {

        Map<String, String> requestParmas = request.getOrginalParmas();
        if (requestParmas != null) {
            FormBody.Builder builder = new FormBody.Builder();

            Set<String> keySet = requestParmas.keySet();
            Iterator<String> iterator = keySet.iterator();
            while (iterator.hasNext()) {
                String key = iterator.next();
                builder.add(key, requestParmas.get(key));
            }
            FormBody formBody = builder.build();

            Request okRequest = new Request.Builder()
                    .url(request.getUrl())
                    .post(formBody)
                    .build();
            Call call = mOkHttpClient.newCall(okRequest);
            call.enqueue(new Callback() {
                @Override
                public void onFailure(Call call, IOException e) {
                    InsuranceLogger.d("net", "onfail");

                    if (responseHandler != null) {
                        responseHandler.onFailure(request, e);

                    }

                }

                @Override
                public void onResponse(Call call, Response response) throws IOException {
                    try {
                        InsuranceLogger.d("net", "onsuccess");
                        InputStream inputStream = response.body().byteStream();
                        if (responseHandler != null) {
                            T t = (T) responseHandler.parseResponse(request, inputStream,
                                    response.body().contentLength());

                            responseHandler.onSuccess(request, response.code(), t);


                        }
                        response.body().close();
                    } catch (Exception e) {
                        e.printStackTrace();
                    } finally {
                    }
                }
            });

        }

    }

    /**
     * get请求
     */
    private void requestByGet(IRequest request, IResponseHandler responseHandler) {
        try {
            Request okRequest = new Request.Builder().url(request.getUrl()).build();
            Call call = mOkHttpClient.newCall(okRequest);
            call.enqueue(new Callback() {
                @Override
                public void onFailure(Call call, IOException e) {
                    Log.e("net", "net erro");
                }

                @Override
                public void onResponse(Call call, Response response) throws IOException {
                    String content = response.body().string();
                    System.out.println("content=" + content);
                }
            });
        } catch (Exception e) {
            e.printStackTrace();
        }

    }


}
