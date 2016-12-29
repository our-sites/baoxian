package com.common.insurance.utils;

import android.text.TextUtils;

import java.io.BufferedInputStream;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.security.MessageDigest;
import java.util.zip.GZIPOutputStream;

/**
 * 字符串处理
 * 
 */
public class StringUtil {

	private static final char[] DIGITS_LOWER = { '0', '1', '2', '3', '4', '5',
			'6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f' };

	public static String md5(String str) {

		if (TextUtils.isEmpty(str)) {
			return "";
		}

		try {
			MessageDigest messageDigest = MessageDigest.getInstance("MD5");
			messageDigest.update(str.getBytes());
			return new String(encodeHex(messageDigest.digest()));
		} catch (Exception e) {
		}

		return str;
	}

	private static char[] encodeHex(final byte[] data) {

		final int l = data.length;
		final char[] out = new char[l << 1];

		for (int i = 0, j = 0; i < l; i++) {
			out[j++] = DIGITS_LOWER[(0xF0 & data[i]) >>> 4];
			out[j++] = DIGITS_LOWER[0x0F & data[i]];
		}
		return out;
	}

    /**
     * GZIP压缩
     *
     * @param data
     * @return
     */
    public static byte[] compressToByte(byte[] data) throws Exception {

        if (data == null || data.length == 0) {
            return null;
        }

        ByteArrayOutputStream out = new ByteArrayOutputStream();
        GZIPOutputStream zos;

        BufferedInputStream bis = new BufferedInputStream(new ByteArrayInputStream(data));

        byte[] buf = new byte[512];
        int len;

        try {
            zos = new GZIPOutputStream(out);

            while ((len = bis.read(buf)) != -1) {
                zos.write(buf, 0, len);
                zos.flush();
            }

            bis.close();
            zos.close();

            return out.toByteArray();
        } finally {
            if (out != null) {
                try {
                    out.close();
                } catch (Exception e2) {
                }
            }
        }
    }
}
