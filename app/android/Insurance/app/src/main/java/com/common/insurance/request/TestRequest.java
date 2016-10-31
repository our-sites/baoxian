package com.common.insurance.request;

import android.content.Context;
import android.os.Message;

import com.common.insurance.model.ResultModel;
import com.common.insurance.utils.InsuranceConstans;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.Map;

/**
 * Created by wangyongchao on 16/10/19.
 */
public class TestRequest extends BaseBusinessRequest {


    public TestRequest(Context context) {
        super(context);
    }

    public TestRequest(Context context, Message message) {
        super(context, message);
    }

    public TestRequest(Context context, Map<String, String> params) {
        super(context, params);
    }

    public TestRequest(Context context, Map<String, String> params, Message message) {
        super(context, params, message);
    }

    @Override
    protected String createRequestHostPrefix() {
        return InsuranceConstans.TEST_WEATHER_URL;
    }

    @Override
    protected String createRequestHostPostfix() {
        return null;
    }

    @Override
    protected Object parseResponse(Object data) {

        ResultModel resultModel = null;

        try {
            JSONObject json = new JSONObject(data.toString());

            if (json.has("result")) {
                JSONArray result = json.getJSONArray("result");
//
//                GsonBuilder builder = new GsonBuilder();
//                // 不转换没有 @Expose 注解的字段
//                builder.excludeFieldsWithoutExposeAnnotation();
//                Gson gson = builder.create();
//                @SuppressWarnings("unchecked")
//                ArrayList<GoodsCategory> items = gson
//                        .fromJson(result.toString(),
//                                new TypeToken<ArrayList<GoodsCategory>>() {
//                                }.getType());

//                resultModel.mObj = items;
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return resultModel;

    }


}
