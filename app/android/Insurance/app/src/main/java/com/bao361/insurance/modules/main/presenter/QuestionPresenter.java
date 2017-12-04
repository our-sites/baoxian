package com.bao361.insurance.modules.main.presenter;

import android.os.Handler;
import android.os.Message;

import com.bao361.insurance.base.AbsBusinessPresenter;
import com.bao361.insurance.model.WeatherInfo;
import com.bao361.insurance.modules.main.models.QuestionModel;
import com.bao361.insurance.modules.main.viewimpl.MainView;
import com.bao361.insurance.modules.main.viewimpl.QuestionView;
import com.bao361.insurance.net.RequestError;
import com.bao361.insurance.request.BaseBusinessRequest;
import com.bao361.insurance.request.LoadCallback;
import com.bao361.insurance.request.TestRequest;
import com.bao361.insurance.ui.recycler.LoadHelper;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class QuestionPresenter extends AbsBusinessPresenter<QuestionView> {

    public QuestionPresenter() {
    }

    @Override
    protected void onSuccess(int what, Object response) {
        super.onSuccess(what, response);
        mView.setLoadingIndicator(false);
        mView.refresh();

    }

    @Override
    protected void onFail(int what, Object error) {
        super.onFail(what, error);
        mView.setLoadingIndicator(false);

    }

    public void sendEncapsulationPost() {
        mView.setLoadingIndicator(true);

        Map<String, String> map = new HashMap<>();
        map.put("ip", "58.215.185.154");
        map.put("dtype", "json");
        map.put("key", "177038539bb5e9c91c8a1443145d3765");
        //// TODO: 16/12/20 将来换成rxjava
        BaseBusinessRequest request = new TestRequest(map, new LoadCallback<WeatherInfo>() {
            @Override
            public void onLoadSuccess(WeatherInfo weatherInfo) {

            }

            @Override
            public void onLoadFail(RequestError error) {


            }
        });
        request.execute();

    }

    private Handler handler = new Handler() {
        @Override
        public void handleMessage(Message msg) {
            ArrayList<QuestionModel> data = getData();
            mView.setData(data);
            mView.setLoadingIndicator(false);
        }
    };

    public void loadData() {
        mView.setLoadingIndicator(true);
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    Thread.sleep(500);
                    Message message = handler.obtainMessage();
                    handler.sendEmptyMessage(0);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }).start();


    }

    private ArrayList<QuestionModel> getData() {
        ArrayList<QuestionModel> models = new ArrayList<>();

        for (int i = 0; i < 20; i++) {
            QuestionModel model = new QuestionModel();
            model.name = "名称" + i;
            model.answerNum = 30 + i;
            model.area = "北京";
            model.question = "问题问题问题问题问题问题问题问题问题" + i;
            model.date = "2017-03-21";
            model.userImg = "https://sa.geilicdn.com/udc_bed6cf977b6908467f2f19beadbd7929.jpg";

            models.add(model);

        }
        return models;
    }
}
