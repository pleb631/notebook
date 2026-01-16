#pragma once
#include <opencv2/dnn.hpp>
#include <opencv2/opencv.hpp>
#include <iostream>


void blur_demo(cv::Mat& image) {
	cv::Mat dst;
	cv::blur(image, dst, cv::Size(15, 15), cv::Point(-1, -1));
	cv::GaussianBlur(image, dst, cv::Size(0, 0), 15);
	cv::bilateralFilter(image, dst, 0, 100, 10); //双边模糊
	cv::flip(image, dst, -1);
	cv::resize(image, dst, cv::Size(image.cols / 2, image.rows / 2), 0, 0, cv::INTER_LINEAR);
}

void bitwise_demo(cv::Mat& image) {
	cv::Mat m1 = cv::Mat::zeros(cv::Size(256, 256), CV_8UC3);
	cv::Mat m2 = cv::Mat::zeros(cv::Size(256, 256), CV_8UC3);
	cv::rectangle(m1, cv::Rect(100, 100, 80, 80), cv::Scalar(255, 255, 0), -1, cv::LINE_8, 0);
	cv::imshow("m1", m1);
	cv::imshow("m2", m2);
	cv::Mat dst;
	cv::bitwise_xor(m1, m2, dst);//bitwise_or,bitwise_and,bitwise_not
	cv::imshow("像素位操作", dst);
}

namespace cvdemo1 {
	void colorSpace_Demo(cv::Mat& image) {
		cv::Mat gray, hsv;
		cv::cvtColor(image, hsv, cv::COLOR_BGR2HSV);
		// H 0 ~ 180, S, V 
		cv::cvtColor(image, gray, cv::COLOR_BGR2GRAY);

	}

	void mat_creation_demo() {
		// cv::Mat m1, m2;
		// m1 = image.clone();
		// image.copyTo(m2);

		// 创建空白图像
		cv::Mat m3 = cv::Mat::zeros(cv::Size(8, 8), CV_8UC3);
		m3 = cv::Scalar(0, 0, 255);
		std::cout << "width: " << m3.cols << " height: " << m3.rows << " channels: " << m3.channels() << std::endl;
		// std::cout << m3 << std::endl;

		cv::Mat m4;
		m3.copyTo(m4);
		m4 = cv::Scalar(0, 255, 255);
		cv::imshow("图像", m3);
		cv::imshow("图像4", m4);
	}

	void pixel_visit_demo(cv::Mat& image) {
		int w = image.cols;
		int h = image.rows;
		int dims = image.channels();
		/*
		for (int row = 0; row < h; row++) {
			for (int col = 0; col < w; col++) {
				if (dims == 1) { // 灰度图像
					int pv = image.at<uchar>(row, col);
					image.at<uchar>(row, col) = 255 - pv;
				}
				if (dims == 3) { // 彩色图像
					Vec3b bgr = image.at<Vec3b>(row, col);
					image.at<Vec3b>(row, col)[0] = 255 - bgr[0];
					image.at<Vec3b>(row, col)[1] = 255 - bgr[1];
					image.at<Vec3b>(row, col)[2] = 255 - bgr[2];
				}
			}
		}
		*/

		for (int row = 0; row < h; row++) {
			uchar* current_row = image.ptr<uchar>(row);
			for (int col = 0; col < w; col++) {
				if (dims == 1) { // 灰度图像
					int pv = *current_row;
					*current_row++ = 255 - pv;
				}
				if (dims == 3) { // 彩色图像
					*current_row++ = 255 - *current_row;
					*current_row++ = 255 - *current_row;
					*current_row++ = 255 - *current_row;
				}

			}
			break;
		}
		cv::imshow("像素读写演示", image);
	}

	void operators_demo(cv::Mat& image) {
		cv::Mat dst = cv::Mat::zeros(image.size(), image.type());
		cv::Mat m = cv::Mat::zeros(image.size(), image.type());
		m = cv::Scalar(5, 5, 5);

		// 加法
		/*
		int w = image.cols;
		int h = image.rows;
		int dims = image.channels();
		for (int row = 0; row < h; row++) {
			for (int col = 0; col < w; col++) {
				Vec3b p1 = image.at<Vec3b>(row, col);
				Vec3b p2 = m.at<Vec3b>(row, col);
				dst.at<Vec3b>(row, col)[0] = saturate_cast<uchar>(p1[0] + p2[0]);
				dst.at<Vec3b>(row, col)[1] = saturate_cast<uchar>(p1[1] + p2[1]);
				dst.at<Vec3b>(row, col)[2] = saturate_cast<uchar>(p1[2] + p2[2]);
			}
		}
		*/
		cv::divide(image, m, dst);

		cv::imshow("加法操作", dst);
	}

	static void on_lightness(int b, void* userdata) {
		cv::Mat image = *((cv::Mat*)userdata);
		cv::Mat dst = cv::Mat::zeros(image.size(), image.type());
		cv::Mat m = cv::Mat::zeros(image.size(), image.type());
		cv::addWeighted(image, 1.0, m, 0, b, dst);
		cv::imshow("亮度与对比度调整", dst);
	}

	static void on_contrast(int b, void* userdata) {
		cv::Mat image = *((cv::Mat*)userdata);
		cv::Mat dst = cv::Mat::zeros(image.size(), image.type());
		cv::Mat m = cv::Mat::zeros(image.size(), image.type());
		double contrast = b / 100.0;
		cv::addWeighted(image, contrast, m, 0.0, 0, dst);
		cv::imshow("亮度与对比度调整", dst);
	}

	void tracking_bar_demo(cv::Mat& image) {
		cv::namedWindow("亮度与对比度调整", cv::WINDOW_AUTOSIZE);
		int lightness = 50;
		int max_value = 100;
		int contrast_value = 100;
		cv::createTrackbar("Value Bar:", "亮度与对比度调整", &lightness, max_value, on_lightness, (void*)(&image));
		cv::createTrackbar("Contrast Bar:", "亮度与对比度调整", &contrast_value, 200, on_contrast, (void*)(&image));
	}

	void key_demo(cv::Mat& image) {
		cv::Mat dst = cv::Mat::zeros(image.size(), image.type());
		while (true) {
			int c = cv::waitKey(100);
			if (c == 27) { // 退出
				break;
			}
			if (c == 49) { // Key #1
				std::cout << "you enter key # 1 " << std::endl;
				cv::cvtColor(image, dst, cv::COLOR_BGR2GRAY);
			}
			if (c == 50) { // Key #2
				std::cout << "you enter key # 2 " << std::endl;
				cv::cvtColor(image, dst, cv::COLOR_BGR2HSV);
			}
			if (c == 51) { // Key #3
				std::cout << "you enter key # 3 " << std::endl;
				dst = cv::Scalar(50, 50, 50);
				cv::add(image, dst, dst);
			}
			cv::imshow("键盘响应", dst);
		}
	}

	void color_style_demo(cv::Mat& image) {
		int colormap[] = {
			cv::COLORMAP_AUTUMN,
			cv::COLORMAP_BONE,
			cv::COLORMAP_JET,
			cv::COLORMAP_WINTER,
			cv::COLORMAP_RAINBOW,
			cv::COLORMAP_OCEAN,
			cv::COLORMAP_SUMMER,
			cv::COLORMAP_SPRING,
			cv::COLORMAP_COOL,
			cv::COLORMAP_PINK,
			cv::COLORMAP_HOT,
			cv::COLORMAP_PARULA,
			cv::COLORMAP_MAGMA,
			cv::COLORMAP_INFERNO,
			cv::COLORMAP_PLASMA,
			cv::COLORMAP_VIRIDIS,
			cv::COLORMAP_CIVIDIS,
			cv::COLORMAP_TWILIGHT,
			cv::COLORMAP_TWILIGHT_SHIFTED
		};

		cv::Mat dst;
		int index = 0;
		while (true) {
			int c = cv::waitKey(500);
			if (c == 27) { // 退出
				break;
			}
			cv::applyColorMap(image, dst, colormap[index % 19]);
			index++;
			cv::imshow("颜色风格", dst);
		}
	}



	void channels_demo(cv::Mat& image) {
		std::vector<cv::Mat> mv;
		cv::split(image, mv);
		cv::imshow("蓝色", mv[0]);
		cv::imshow("绿色", mv[1]);
		cv::imshow("红色", mv[2]);

		cv::Mat dst;
		//mv[0] = 0;
		mv[1] = 0;
		cv::merge(mv, dst);
		cv::imshow("红色", dst);

		int from_to[] = { 0, 2, 1,1, 2, 0 };
		cv::mixChannels(&image, 1, &dst, 1, from_to, 3);
		cv::imshow("通道混合", dst);
	}

	void inrange_demo(cv::Mat& image) {
		cv::Mat hsv;
		cv::cvtColor(image, hsv, cv::COLOR_BGR2HSV);
		cv::Mat mask;
		cv::inRange(hsv, cv::Scalar(77, 77, 77), cv::Scalar(180, 180, 180), mask);

		cv::Mat redback = cv::Mat::zeros(image.size(), image.type());
		redback = cv::Scalar(40, 40, 200);
		//cv::bitwise_not(mask, mask);
		cv::imshow("mask", mask);
		image.copyTo(redback, mask);
		cv::imshow("roi区域提取", redback);
	}

	void pixel_statistic_demo(cv::Mat& image) {
		double minv, maxv;
		cv::Point minLoc, maxLoc;
		std::vector<cv::Mat> mv;
		cv::split(image, mv);
		for (int i = 0; i < mv.size(); i++) {
			minMaxLoc(mv[i], &minv, &maxv, &minLoc, &maxLoc, cv::Mat());
			std::cout << "No. channels:" << i << " min value:" << minv << " max value:" << maxv << std::endl;
		}
		cv::Mat mean, stddev;
		cv::Mat redback = cv::Mat::zeros(image.size(), image.type());
		redback = cv::Scalar(40, 40, 200);
		cv::meanStdDev(redback, mean, stddev);
		cv::imshow("redback", redback);
		std::cout << "means:" << mean << std::endl;
		std::cout << " stddev:" << stddev << std::endl;
	}

	void drawing_demo(cv::Mat& image) {
		cv::Rect rect;
		rect.x = 100;
		rect.y = 100;
		rect.width = 250;
		rect.height = 300;
		cv::Mat bg = cv::Mat::zeros(image.size(), image.type());
		cv::rectangle(bg, rect, cv::Scalar(0, 0, 255), -1, 8, 0);
		cv::circle(bg, cv::Point(350, 400), 15, cv::Scalar(255, 0, 0), -1, 8, 0);
		cv::line(bg, cv::Point(100, 100), cv::Point(350, 400), cv::Scalar(0, 255, 0), 4, cv::LINE_AA, 0);
		cv::RotatedRect rrt;
		rrt.center = cv::Point(200, 200);
		rrt.size = cv::Size(100, 200);
		rrt.angle = 90.0;
		cv::ellipse(bg, rrt, cv::Scalar(0, 255, 255), 2, 8);
		cv::Mat dst;
		cv::addWeighted(image, 0.7, bg, 0.3, 0, dst);
		cv::imshow("绘制演示", bg);
	}

	void random_drawing() {
		cv::Mat canvas = cv::Mat::zeros(cv::Size(512, 512), CV_8UC3);
		int w = canvas.cols;
		int h = canvas.rows;
		cv::RNG rng(12345);
		while (true) {
			int c = cv::waitKey(10);
			if (c == 27) { // 退出
				break;
			}
			int x1 = rng.uniform(0, w);
			int y1 = rng.uniform(0, h);
			int x2 = rng.uniform(0, w);
			int y2 = rng.uniform(0, h);
			int b = rng.uniform(0, 255);
			int g = rng.uniform(0, 255);
			int r = rng.uniform(0, 255);
			// canvas = cv::Scalar(0, 0, 0);
			cv::line(canvas, cv::Point(x1, y1), cv::Point(x2, y2), cv::Scalar(b, g, r), 1, cv::LINE_AA, 0);
			cv::imshow("随机绘制演示", canvas);
		}
	}

	void polyline_drawing_demo() {
		cv::Mat canvas = cv::Mat::zeros(cv::Size(512, 512), CV_8UC3);
		int w = canvas.cols;
		int h = canvas.rows;
		cv::Point p1(100, 100);
		cv::Point p2(300, 150);
		cv::Point p3(300, 350);
		cv::Point p4(250, 450);
		cv::Point p5(50, 450);
		std::vector<cv::Point> pts;
		pts.push_back(p1);
		pts.push_back(p2);
		pts.push_back(p3);
		pts.push_back(p3);
		pts.push_back(p4);
		pts.push_back(p5);
		// polylines(canvas, pts, true, cv::Scalar(0, 255, 0), -1, 8, 0);
		std::vector<std::vector<cv::Point>> contours;
		contours.push_back(pts);
		cv::drawContours(canvas, contours, 0, cv::Scalar(0, 0, 255), -1, 8);
		cv::imshow("绘制多边形", canvas);
	}

	cv::Point sp(-1, -1);
	cv::Point ep(-1, -1);
	cv::Mat temp;
	static void on_draw(int event, int x, int y, int flags, void* userdata) {
		cv::Mat image = *((cv::Mat*)userdata);
		if (event == cv::EVENT_LBUTTONDOWN) {
			sp.x = x;
			sp.y = y;
			std::cout << "start point:" << sp << std::endl;
		}
		else if (event == cv::EVENT_LBUTTONUP) {
			ep.x = x;
			ep.y = y;
			int dx = ep.x - sp.x;
			int dy = ep.y - sp.y;
			std::cout << "x:" << sp << "  y:" << dx << "  " << dy << std::endl;
			if (dx > 0 && dy > 0) {

				cv::Rect box(sp.x, sp.y, dx, dy);
				temp.copyTo(image);
				cv::imshow("ROI区域", image(box));
				cv::rectangle(image, box, cv::Scalar(0, 0, 255), 2, 8, 0);
				cv::imshow("鼠标绘制", image);
				// ready for next drawing
				sp.x = -1;
				sp.y = -1;
			}
		}
		else if (event == cv::EVENT_MOUSEMOVE) {
			if (sp.x > 0 && sp.y > 0) {
				ep.x = x;
				ep.y = y;
				int dx = ep.x - sp.x;
				int dy = ep.y - sp.y;
				if (dx > 0 && dy > 0) {
					cv::Rect box(sp.x, sp.y, dx, dy);
					temp.copyTo(image);

					cv::rectangle(image, box, cv::Scalar(0, 0, 255), 2, 8, 0);
					cv::imshow("鼠标绘制", image);
				}
			}
		}
	}

	void mouse_drawing_demo(cv::Mat& image) {
		cv::namedWindow("鼠标绘制", cv::WINDOW_AUTOSIZE);
		cv::setMouseCallback("鼠标绘制", on_draw, (void*)(&image));
		cv::imshow("鼠标绘制", image);
		temp = image.clone();
	}

	void norm_demo(cv::Mat& image) {
		cv::Mat dst;
		std::cout << image.type() << std::endl;
		image.convertTo(image, CV_32F);
		std::cout << image.type() << std::endl;
		cv::normalize(image, dst, 1.0, 0, cv::NORM_MINMAX);
		std::cout << dst.type() << std::endl;
		cv::imshow("图像数据归一化", dst);
		// CV_8UC3, CV_32FC3
	}


	void rotate_demo(cv::Mat& image) {
		cv::Mat dst, M;
		size_t w = image.cols;
		size_t h = image.rows;
		M = cv::getRotationMatrix2D(cv::Point2f(w / 2, h / 2), 45, 1.0);
		double cos = abs(M.at<double>(0, 0));
		double sin = abs(M.at<double>(0, 1));
		double nw = cos * w + sin * h;
		double nh = sin * w + cos * h;
		double x = (w - nw) / 2;
		double y = (h - nh) / 2;
		M.at<double>(0, 2) += x;
		M.at<double>(1, 2) += y;
		cv::warpAffine(image, dst, M, cv::Size(nw, nh), cv::INTER_LINEAR, 0, cv::Scalar(255, 255, 0));
		cv::imshow("旋转演示", dst);
	}

	void video_demo(cv::Mat& image) {
		cv::VideoCapture capture("D:/images/video/example_dsh.mp4");
		int frame_width = capture.get(cv::CAP_PROP_FRAME_WIDTH);
		int frame_height = capture.get(cv::CAP_PROP_FRAME_HEIGHT);
		int count = capture.get(cv::CAP_PROP_FRAME_COUNT);
		double fps = capture.get(cv::CAP_PROP_FPS);
		std::cout << "frame width:" << frame_width << std::endl;
		std::cout << "frame height:" << frame_height << std::endl;
		std::cout << "FPS:" << fps << std::endl;
		std::cout << "Number of Frames:" << count << std::endl;
		cv::VideoWriter writer("D:/test.mp4", capture.get(cv::CAP_PROP_FOURCC), fps, cv::Size(frame_width, frame_height), true);
		cv::Mat frame;
		while (true) {
			capture.read(frame);
			cv::flip(frame, frame, 1);
			if (frame.empty()) {
				break;
			}
			cv::imshow("frame", frame);
			colorSpace_Demo(frame);
			writer.write(frame);
			// TODO: do something....
			int c = cv::waitKey(1);
			if (c == 27) { // 退出
				break;
			}
		}

		// release
		capture.release();
		writer.release();
	}

	void histogram_demo(cv::Mat& image) {
		// 三通道分离
		std::vector<cv::Mat> bgr_plane;
		cv::split(image, bgr_plane);
		// 定义参数变量
		const int channels[1] = { 0 };
		const int bins[1] = { 256 };
		float hranges[2] = { 0,255 };
		const float* ranges[1] = { hranges };
		cv::Mat b_hist;
		cv::Mat g_hist;
		cv::Mat r_hist;
		// 计算Blue, Green, Red通道的直方图
		cv::calcHist(&bgr_plane[0], 1, 0, cv::Mat(), b_hist, 1, bins, ranges);
		cv::calcHist(&bgr_plane[1], 1, 0, cv::Mat(), g_hist, 1, bins, ranges);
		cv::calcHist(&bgr_plane[2], 1, 0, cv::Mat(), r_hist, 1, bins, ranges);

		// 显示直方图
		int hist_w = 512;
		int hist_h = 400;
		int bin_w = cvRound((double)hist_w / bins[0]);
		cv::Mat histImage = cv::Mat::zeros(hist_h, hist_w, CV_8UC3);
		// 归一化直方图数据
		cv::normalize(b_hist, b_hist, 0, histImage.rows, cv::NORM_MINMAX, -1, cv::Mat());
		cv::normalize(g_hist, g_hist, 0, histImage.rows, cv::NORM_MINMAX, -1, cv::Mat());
		cv::normalize(r_hist, r_hist, 0, histImage.rows, cv::NORM_MINMAX, -1, cv::Mat());
		// 绘制直方图曲线
		for (int i = 1; i < bins[0]; i++) {
			cv::line(histImage, cv::Point(bin_w * (i - 1), hist_h - cvRound(b_hist.at<float>(i - 1))),
				cv::Point(bin_w * (i), hist_h - cvRound(b_hist.at<float>(i))), cv::Scalar(255, 0, 0), 2, 8, 0);
			cv::line(histImage, cv::Point(bin_w * (i - 1), hist_h - cvRound(g_hist.at<float>(i - 1))),
				cv::Point(bin_w * (i), hist_h - cvRound(g_hist.at<float>(i))), cv::Scalar(0, 255, 0), 2, 8, 0);
			cv::line(histImage, cv::Point(bin_w * (i - 1), hist_h - cvRound(r_hist.at<float>(i - 1))),
				cv::Point(bin_w * (i), hist_h - cvRound(r_hist.at<float>(i))), cv::Scalar(0, 0, 255), 2, 8, 0);
		}
		// 显示直方图
		cv::namedWindow("Histogram Demo", cv::WINDOW_AUTOSIZE);
		cv::imshow("Histogram Demo", histImage);
	}

	void histogram_2d_demo(cv::Mat& image) {
		// 2D 直方图
		cv::Mat hsv, hs_hist;
		cv::cvtColor(image, hsv, cv::COLOR_BGR2HSV);
		int hbins = 30, sbins = 32;
		int hist_bins[] = { hbins, sbins };
		float h_range[] = { 0, 180 };
		float s_range[] = { 0, 256 };
		const float* hs_ranges[] = { h_range, s_range };
		int hs_channels[] = { 0, 1 };
		cv::calcHist(&hsv, 1, hs_channels, cv::Mat(), hs_hist, 2, hist_bins, hs_ranges, true, false);
		double maxVal = 0;
		cv::minMaxLoc(hs_hist, 0, &maxVal, 0, 0);
		int scale = 10;
		cv::Mat hist2d_image = cv::Mat::zeros(sbins * scale, hbins * scale, CV_8UC3);
		for (int h = 0; h < hbins; h++) {
			for (int s = 0; s < sbins; s++)
			{
				float binVal = hs_hist.at<float>(h, s);
				int intensity = cvRound(binVal * 255 / maxVal);
				cv::rectangle(hist2d_image, cv::Point(h * scale, s * scale),
					cv::Point((h + 1) * scale - 1, (s + 1) * scale - 1),
					cv::Scalar::all(intensity),
					-1);
			}
		}
		cv::applyColorMap(hist2d_image, hist2d_image, cv::COLORMAP_JET);
		cv::imshow("H-S Histogram", hist2d_image);
		cv::imwrite("D:/hist_2d.png", hist2d_image);
	}

	void histogram_eq_demo(cv::Mat& image) {
		cv::Mat gray;
		cv::cvtColor(image, gray, cv::COLOR_BGR2GRAY);
		cv::imshow("灰度图像", gray);
		cv::Mat dst;
		cv::equalizeHist(gray, dst);
		cv::imshow("直方图均衡化演示", dst);
	}





	void face_detection_demo() {
		std::string root_dir = "D:/opencv-4.4.0/opencv/sources/samples/dnn/face_detector/";
		cv::dnn::Net net = cv::dnn::readNetFromTensorflow(root_dir + "opencv_face_detector_uint8.pb", root_dir + "opencv_face_detector.pbtxt");
		cv::VideoCapture capture("D:/images/video/example_dsh.mp4");
		cv::Mat frame;
		while (true) {
			capture.read(frame);
			if (frame.empty()) {
				break;
			}
			cv::Mat blob = cv::dnn::blobFromImage(frame, 1.0, cv::Size(300, 300), cv::Scalar(104, 177, 123), false, false);
			net.setInput(blob);// NCHW
			cv::Mat probs = net.forward(); // 
			cv::Mat detectionMat(probs.size[2], probs.size[3], CV_32F, probs.ptr<float>());
			// 解析结果
			for (int i = 0; i < detectionMat.rows; i++) {
				float confidence = detectionMat.at<float>(i, 2);
				if (confidence > 0.5) {
					int x1 = static_cast<int>(detectionMat.at<float>(i, 3) * frame.cols);
					int y1 = static_cast<int>(detectionMat.at<float>(i, 4) * frame.rows);
					int x2 = static_cast<int>(detectionMat.at<float>(i, 5) * frame.cols);
					int y2 = static_cast<int>(detectionMat.at<float>(i, 6) * frame.rows);
					cv::Rect box(x1, y1, x2 - x1, y2 - y1);
					rectangle(frame, box, cv::Scalar(0, 0, 255), 2, 8, 0);
				}
			}
			cv::imshow("人脸检测演示", frame);
			int c = cv::waitKey(1);
			if (c == 27) { // 退出
				break;
			}
		}


	}
}