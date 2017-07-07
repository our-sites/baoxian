package com.bao361.insurance.imageeagle;

import android.annotation.TargetApi;
import android.app.Activity;
import android.content.Context;
import android.os.Build;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentActivity;

/**
 * @author：wangyongchao on 17/5/10 16:46
 */
public class Eagle {


    public static ICatcher with(Context context) {
        ICatcher iCatcher = new ContextEagleCatcherFactory().createEagleCatcher(context);
        return iCatcher;

    }

    public static ICatcher with(Activity activity) {
        ICatcher catcher = new ActivityEagleCatcherFactory().createEagleCatcher(activity);
        return catcher;
    }

    public static ICatcher with(FragmentActivity activity) {
        ICatcher catcher = new FragmentActivityEagleCatcherFactory().createEagleCatcher(activity);
        return catcher;
    }

    @TargetApi(Build.VERSION_CODES.HONEYCOMB)
    public static ICatcher with(android.app.Fragment fragment) {
        ICatcher catcher = new AppFragmentEagleCatcherFactory().createEagleCatcher(fragment);
        return catcher;
    }

    public static ICatcher with(Fragment fragment) {
        ICatcher catcher = new SupportFragmentEagleCatcherFactory().createEagleCatcher(fragment);
        return catcher;
    }

}
