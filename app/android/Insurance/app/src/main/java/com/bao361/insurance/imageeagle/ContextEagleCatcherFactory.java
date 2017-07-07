package com.bao361.insurance.imageeagle;

import android.content.Context;

/**
 * 创建context类型的图片获取器
 */
public class ContextEagleCatcherFactory extends AbstractEagleCatcherFactory<Context> {


    @Override
    public ICatcher createEagleCatcher(Context context) {
        ICatcher iCatcher = new EagleCatcher(context);
        return iCatcher;
    }
}
