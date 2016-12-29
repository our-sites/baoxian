package com.common.insurance.net;

import java.util.Map;

public interface IRequest {

    /**
     * 请求地址
     *
     * @return
     */
    public String getUrl();

    /**
     * 设置请求地址，暴露用于IP地址轮询
     *
     * @param url
     * @return
     */
    public void setUrl(String url);


    /**
     * 请求方式，目前仅支持Get和POST
     */
    public int getMethod();

    /**
     * 返回请求数据
     *
     * @return
     */
    public Map<String, String> getRequestParmas();


    /**
     * 返回请求的原始数据
     */
    public Map<String, String> getOrginalParmas();

    /**
     * 目前仅支持Get和POST，后续有需求可以扩展
     */
    public interface Method {

        public static final int GET = 0;

        public static final int POST = 1;
    }
}
