package com.common.insurance.imageeagle;

import android.app.Activity;

/**
 * 创建Activity类型的图片获取器
 */
public class ActivityEagleCatcherFactory extends AbstractEagleCatcherFactory<Activity> {


    @Override
    public ICatcher createEagleCatcher(Activity activity) {
        ICatcher iCatcher = new EagleCatcher(activity);
        return iCatcher;
    }
}
