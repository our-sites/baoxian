package com.common.insurance.net;

import java.io.IOException;
import java.io.InputStream;


public class DefaultResponseHandler extends IResponseHandler<byte[]> {


    protected static int DEFAULT_POOL_SIZE = 4 * 1024;

    @Override
    public void onStart() {
    }

    @Override
    public void onFinish() {
    }

    @Override
    public void onCancel() {
    }

    @Override
    public void onProgress(int progress) {
    }

    @Override
    public void onSuccess(IRequest request, int statusCode,
                          byte[] responseBytes) {


    }

    @Override
    public void onFailure(IRequest request, int statusCode, byte[] responseBody, Throwable error) {
    }

    @Override
    public void onFailure(IRequest request, Throwable error) {
        onFailure(request, -1, null, error);
    }

    @Override
    public void onRetry() {
    }


    @Override
    public byte[] parseResponse(IRequest request, InputStream inputStream,
                                long contentLength) throws Exception {

        ByteArrayPool pool = new ByteArrayPool(DEFAULT_POOL_SIZE);
        PoolingByteArrayOutputStream bytes = new PoolingByteArrayOutputStream(pool);

        byte[] buffer = null;

        try {

            if (inputStream == null) {
                throw new IOException("obtain nothing，something is wrong");
            }

            buffer = pool.getBuf(1024);
            int count = 0;
            int total = 0;

            while ((count = inputStream.read(buffer)) != -1) {

                bytes.write(buffer, 0, count);

                total = total + count;

                publishProgress(contentLength <= 0 ? 100
                        : (int) (total * 100 / contentLength));
            }


            byte[] data = bytes.toByteArray();

            return data;
        } catch (OutOfMemoryError e) {
            System.gc();
            throw new IOException(
                    "HTTP entity too large to be buffered in memory");
        } finally {
            pool.returnBuf(buffer);
            bytes.close();
        }
    }
}
