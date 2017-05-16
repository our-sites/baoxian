package com.common.insurance.imageeagle;

import android.net.Uri;
import android.widget.ImageView;

import java.io.File;

/**
 * @author：wangyongchao on 17/5/10 18:17
 */
public interface ICatcher {

    /**
     * 通过url加载
     *
     * @param string
     * @return
     */
    ICatcher load(String string);

    /**
     * 通过文件加载
     *
     * @param file
     * @return
     */
    ICatcher load(File file);


    /**
     * 通过uri
     * 加载
     *
     * @param uri
     * @return
     */
    ICatcher load(Uri uri);


    /**
     * 通过资源id加载
     *
     * @param id
     * @return
     */
    ICatcher load(Integer id);

    ICatcher asBitmap();

    ICatcher asGif();

    ICatcher placeholder(int resourceId);

    ICatcher diskCacheStrategy(EagleDiskCacheStrategy diskCacheStrategy);

    ICatcher error(int resourceId);

    ICatcher size(int width, int height);

    ICatcher into(ImageView imageView);

}
