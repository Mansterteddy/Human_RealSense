#include <iostream>
#include <string>
#include <sstream>
#include "rs.hpp"
#include "opencv2/opencv.hpp"
#include "opencv2/highgui.hpp"

using namespace std;

int const INPUT_WIDTH = 640;
int const INPUT_HEIGHT = 480;
int const FRAMERATE = 30;

char* const WINDOW_DEPTH = "Depth Image";
char* const WINDOW_RGB = "RGB Image";

rs::context _rs_ctx;
rs::device& _rs_camera = *_rs_ctx.get_device(0);
rs::intrinsics _depth_intrin;
rs::intrinsics _color_intrin;
bool _loop = true;
bool _capture = false;
int cur_frame = 0;

bool initialize_streaming()
{
    bool success = false;
    if(_rs_ctx.get_device_count() > 0)
    {
        _rs_camera.enable_stream(rs::stream::color, INPUT_WIDTH, INPUT_HEIGHT, rs::format::rgb8, FRAMERATE);
        _rs_camera.enable_stream(rs::stream::depth, INPUT_WIDTH, INPUT_HEIGHT, rs::format::z16, FRAMERATE);
        _rs_camera.start();

        success = true;
    }
    return success;
}

static void onMouse(int event, int x, int y, int, void* window_name)
{
    if(event == cv::EVENT_LBUTTONDOWN)
    {
        _loop = false;
    }
}

void setup_windows()
{
    cv::namedWindow(WINDOW_DEPTH, 0);
    cv::namedWindow(WINDOW_RGB, 0);

    cv::setMouseCallback(WINDOW_DEPTH, onMouse, WINDOW_DEPTH);
    cv::setMouseCallback(WINDOW_RGB, onMouse, WINDOW_RGB);
}

bool display_next_frame()
{
    _depth_intrin = _rs_camera.get_stream_intrinsics(rs::stream::depth);
    _color_intrin = _rs_camera.get_stream_intrinsics(rs::stream::color);

    cv::Point point_a = cv::Point(79, 0);
    cv::Point point_b = cv::Point(559, 479);

    //Create depth image
    cv::Mat depth16(_depth_intrin.height, _depth_intrin.width, CV_16U, (uchar *)_rs_camera.get_frame_data(rs::stream::depth_aligned_to_color));
    cv::Mat rgb(_color_intrin.height, _color_intrin.width, CV_8UC3, (uchar *)_rs_camera.get_frame_data(rs::stream::color));

    if(_capture)
    {
        stringstream sstream;
        string str;
        sstream << cur_frame;
        sstream >> str;

        cv::Rect rect(79, 0, 480, 480);
        cv::Mat mid_image = depth16(rect);
        cv::Mat save_image;
        cv::resize(mid_image, save_image, cv::Size(256, 256));

        string depth_file = "/Users/manster/Desktop/Human_RealSense/Human_RealSense_Capture/distance_img/" + str + "_distance.png";
        cv::imwrite(depth_file, save_image);
    }

    cv::Mat depth8u = depth16;
    depth8u.convertTo(depth8u, CV_8UC1, 255.0 / 1000);

    cv::rectangle(depth8u, point_a, point_b, cv::Scalar(255, 255, 0));
    cv::imshow(WINDOW_DEPTH, depth8u);

    if(_capture)
    {
        stringstream sstream;
        string str;
        sstream << cur_frame;
        sstream >> str;

        cv::Rect rect(79, 0, 480, 480);
        cv::Mat mid_image = depth8u(rect);
        cv::Mat save_image;
        cv::resize(mid_image, save_image, cv::Size(256, 256));

        string depth_file = "/Users/manster/Desktop/Human_RealSense/Human_RealSense_Capture/d_img/" + str + "_d.jpg";
        cv::imwrite(depth_file, save_image);
    }

    cv::cvtColor(rgb, rgb, cv::COLOR_BGR2RGB);
    cv::rectangle(rgb, point_a, point_b, cv::Scalar(255, 255, 0));
    cv::imshow(WINDOW_RGB, rgb);

    if(_capture)
    {
        stringstream sstream;
        string str;
        sstream << cur_frame;
        sstream >> str;

        cv::Rect rect(79, 0, 480, 480);
        cv::Mat mid_image = rgb(rect);
        cv::Mat save_image;
        cv::resize(mid_image, save_image, cv::Size(256, 256));

        string color_file = "/Users/manster/Desktop/Human_RealSense/Human_RealSense_Capture/c_img/" + str + "_c.jpg";
        cv::imwrite(color_file, save_image);
    }

    cur_frame += 1;

    return true;
}

float getDistance(int x, int y)
{
    uint16_t * depthImage = (uint16_t *)_rs_camera.get_frame_data(rs::stream::depth_aligned_to_color);
    float scale = _rs_camera.get_depth_scale();
    rs::intrinsics depthIntrin = _rs_camera.get_stream_intrinsics(rs::stream::depth_aligned_to_color);
    uint16_t depthValue = depthImage[y * depthIntrin.width + x];
    float depthMeters = depthValue * scale;
    //std::cout<<"Get Distance: scale is: "<<scale<<std::endl;
    //std::cout<<"Get Distance: depthValue is: "<<depthValue<<std::endl;
    //std::cout<<"Get Distance: depthMeters is: "<<depthMeters<<std::endl;
    return depthMeters;
}

int main() try
{
    rs::log_to_console(rs::log_severity::warn);

    if(!initialize_streaming())
    {
        cout<<"Unable to locate a camera"<<std::endl;
        rs::log_to_console(rs::log_severity::fatal);
        return EXIT_FAILURE;
    }

    setup_windows();

    char keyboard_event = 'a';

    float scale = _rs_camera.get_depth_scale();
    cout<<"Scale is: "<<scale<<endl;

    while(_loop)
    {
        if(_rs_camera.is_streaming())
            _rs_camera.wait_for_frames();

        keyboard_event = cvWaitKey(1);

        if(keyboard_event == 's')
        {
            cout<<"Start Capturing..."<<endl;
            _capture = true;
        }
        else if(keyboard_event == 'e')
        {
            cout<<"End Capturing..."<<endl;
            _capture = false;
        }

        display_next_frame();

        //float  depth = getDistance(320, 240);
    }

    _rs_camera.stop();
    cv::destroyAllWindows();

    return EXIT_SUCCESS;

} catch (const rs::error & e)
{
    std::cerr << "RealSense error calling " << e.get_failed_function() << "(" << e.get_failed_args() << "):\n   " << e.what() << endl;
    return EXIT_FAILURE;
}
catch(const std::exception & e)
{
    std::cerr << e.what() << std::endl;
    return EXIT_FAILURE;
}