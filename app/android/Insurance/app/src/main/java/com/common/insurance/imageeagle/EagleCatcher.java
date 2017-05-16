package com.common.insurance.imageeagle;

import android.annotation.TargetApi;
import android.app.Activity;
import android.content.Context;
import android.net.Uri;
import android.os.Build;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentActivity;
import android.widget.ImageView;

import com.bumptech.glide.DrawableTypeRequest;
import com.bumptech.glide.GenericRequestBuilder;
import com.bumptech.glide.Glide;
import com.bumptech.glide.RequestManager;
import com.bumptech.glide.load.engine.DiskCacheStrategy;

import java.io.File;

/**
 * @author：wangyongchao on 17/5/10 18:18
 */
public class EagleCatcher implements ICatcher {
    private RequestManager requestManager;

    private String url = "";
    private Uri uri;
    private File file;
    private Integer resId;

    private boolean isBitmap = true;//是否是静态图片
    private boolean isGif;//是否动态图片

    private int placeHoder = -1;//站位图

    private EagleDiskCacheStrategy eagleDiskCacheStrategy = EagleDiskCacheStrategy.NONE;//磁盘缓存策略

    private int errorResId = -1;//发生错误展示的资源

    private int width = -1;//指定图片的宽度
    private int height = -1;//指定图片的高度


    public EagleCatcher(Context context) {
        requestManager = Glide.with(context);

    }

    public EagleCatcher(Activity activity) {
        requestManager = Glide.with(activity);
    }

    public EagleCatcher(FragmentActivity activity) {
        requestManager = Glide.with(activity);
    }

    @TargetApi(Build.VERSION_CODES.HONEYCOMB)
    public  EagleCatcher(android.app.Fragment fragment) {
        requestManager = Glide.with(fragment);

    }

    public EagleCatcher(Fragment fragment) {
        requestManager = Glide.with(fragment);
    }


    @Override
    public ICatcher load(String string) {
        url = string;
        uri = null;
        file = null;
        resId = null;
        return this;
    }


    @Override
    public ICatcher load(File file) {
        url = null;
        uri = null;
        this.file = file;
        resId = null;
        return this;
    }

    @Override
    public ICatcher load(Uri uri) {
        url = null;
        this.uri = uri;
        file = null;
        resId = null;
        return this;
    }

    @Override
    public ICatcher load(Integer id) {
        url = null;
        uri = null;
        file = null;
        resId = id;
        return this;
    }

    @Override
    public ICatcher asBitmap() {

        isBitmap = true;
        isGif = false;
        return this;
    }

    @Override
    public ICatcher asGif() {
        isBitmap = false;
        isGif = true;
        return this;
    }

    @Override
    public ICatcher placeholder(int resourceId) {
        placeHoder = resourceId;
        return this;
    }

    @Override
    public ICatcher diskCacheStrategy(EagleDiskCacheStrategy diskCacheStrategy) {
        this.eagleDiskCacheStrategy = diskCacheStrategy;
        return this;
    }

    @Override
    public ICatcher error(int resourceId) {
        errorResId = resourceId;

        return this;
    }

    @Override
    public ICatcher size(int width, int height) {
        this.width = width;
        this.height = height;
        return this;
    }

    @Override
    public ICatcher into(ImageView imageView) {
        DrawableTypeRequest drawableTypeRequest = null;
        GenericRequestBuilder genericRequestBuilder = null;

        if (url != null) {
            drawableTypeRequest = requestManager.load(url);
        } else if (file != null) {
            drawableTypeRequest = requestManager.load(file);
        } else if (uri != null) {
            drawableTypeRequest = requestManager.load(uri);
        } else if (resId != null) {
            drawableTypeRequest = requestManager.load(resId);
        }

        if (isGif) {
            genericRequestBuilder = drawableTypeRequest.asGif();
        } else if (isBitmap) {
            genericRequestBuilder = drawableTypeRequest.asBitmap();
        }

        if (genericRequestBuilder != null) {
            setProperty(genericRequestBuilder, imageView);
        } else {
            setProperty(drawableTypeRequest, imageView);
        }

        return this;
    }

    private void setProperty(GenericRequestBuilder genericRequestBuilder, ImageView imageView) {
        if (placeHoder != -1) {
            genericRequestBuilder.placeholder(placeHoder);
        }
        DiskCacheStrategy diskCacheStrategy = DiskCacheStrategy.NONE;
        if (eagleDiskCacheStrategy == EagleDiskCacheStrategy.ALL) {
            diskCacheStrategy = DiskCacheStrategy.ALL;
        } else if (eagleDiskCacheStrategy == EagleDiskCacheStrategy.SOURCE) {
            diskCacheStrategy = DiskCacheStrategy.SOURCE;
        } else if (eagleDiskCacheStrategy == EagleDiskCacheStrategy.RESULT) {
            diskCacheStrategy = DiskCacheStrategy.RESULT;
        }
        genericRequestBuilder.diskCacheStrategy(diskCacheStrategy);

        if (errorResId != -1) {
            genericRequestBuilder.error(errorResId);
        }

        if (width != -1 && height != -1) {
            genericRequestBuilder.override(width, height);
        }
        genericRequestBuilder.into(imageView);

    }

}
