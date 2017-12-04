package com.bao361.insurance.share;

import android.content.Context;

import com.bao361.insurance.utils.InsuranceConstans;
import com.tencent.mm.opensdk.modelmsg.SendMessageToWX;
import com.tencent.mm.opensdk.modelmsg.WXMediaMessage;
import com.tencent.mm.opensdk.modelmsg.WXTextObject;
import com.tencent.mm.opensdk.openapi.IWXAPI;
import com.tencent.mm.opensdk.openapi.WXAPIFactory;

/**
 * Created by wangyongchao on 2017/8/31.
 */

public class WXShareManager {

    public final static int FRIEND = 100;
    public final static int FRIEND_GROUP = FRIEND + 1;

    private final static WXShareManager instance = new WXShareManager();
    private static IWXAPI wxapi;

    private WXShareManager() {

    }

    public static WXShareManager getInstance() {
        return instance;
    }

    /**
     * 只需初始化一次
     *
     * @param context
     */
    public void register(Context context) {
        wxapi = WXAPIFactory.createWXAPI(context, InsuranceConstans.APP_ID, true);
        wxapi.registerApp(InsuranceConstans.APP_ID);
    }

    /**
     * 只分享文本内容
     *
     * @param text
     * @param type
     */
    public void shareText(String text, int type) {
        WXTextObject textObject = new WXTextObject();
        textObject.text = text;

        WXMediaMessage msg = new WXMediaMessage();
        msg.mediaObject = textObject;
        msg.description = text;

        SendMessageToWX.Req req = new SendMessageToWX.Req();
        req.transaction = String.valueOf(System.currentTimeMillis());
        req.message = msg;
        if (type == FRIEND) {
            req.scene = SendMessageToWX.Req.WXSceneTimeline;
        } else {
            req.scene = SendMessageToWX.Req.WXSceneSession;
        }
        wxapi.sendReq(req);
    }


}
