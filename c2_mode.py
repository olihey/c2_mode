import sys


def calculate_gcd(x, y):
    while y != 0:
        (x, y) = (y, x % y)
    return x

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('width', type=int, help='width of the screen')
    # parser.add_argument('height', type=int, help='height of the screen')
    # parser.add_argument('hz', type=int, help='refresh rate in Hz', nargs='?', default=60)
    #
    # py_args = parser.parse_args()
    # width = py_args.width
    # height = py_args.height
    # hz = py_args.hz
    #
    # cvt_command_line = ["cvt", str(width), str(height), str(hz)]
    # if 60 == hz:
    #     cvt_command_line.append("-r")
    # mode_line = subprocess.check_output(cvt_command_line).decode("utf8").split("\n")[1]
    # mode_line = [x for x in mode_line.split(" ") if x]

    mode_line = sys.argv[1:]
    print(mode_line)
    width = int(mode_line[3])
    height = int(mode_line[7])
    hz_float = float(mode_line[1].split("_")[1])

    gcd = calculate_gcd(width, height)
    aspect_ratio_num = int(width / gcd)
    aspect_ratio_den = int(height / gcd)

    pixel_clock = float(mode_line[2])
    pixel_clock_1000 = int(pixel_clock * 1000)
    pixel_clock_10000 = int(pixel_clock * 10000)
    pixel_clock_100000 = int(pixel_clock * 100000)
    pixel_clock_1000000 = int(pixel_clock * 1000000)

    # no idea how to calculaet this
    # 48500 was found by looking thru all values
    pixel_clock_aml_str = "%02x" % round(pixel_clock_10000 / 48500)

    h_total = int(mode_line[6])
    h_blank = h_total - width
    h_front = int(mode_line[4]) - width
    h_sync = int(mode_line[5]) - (width + h_front)
    h_back = h_total - (width + h_front + h_sync)
    hsync_polarity = 0 if "-" == mode_line[11][0] else 1

    v_total = int(mode_line[10])
    v_blank = v_total - height
    v_front = int(mode_line[8]) - height
    v_sync = int(mode_line[9]) - (height + v_front)
    v_back = v_total - (height + v_front + v_sync)
    vsync_polarity = 0 if "-" == mode_line[12][0] else 1

    v_freq = int(hz_float * 1000)
    h_freq = int(hz_float * (v_total - 1))
    hz = int(round(hz_float))    

    # 1
    print("\n\n\n1) drivers/amlogic/clk/gxbb_hdmi_clk.c: (around line 125)\n")
    print("    HPLL_FVCO_RATE({pixel_clock_10000}, 0x{pixel_clock_aml_str}, 0x1, 0, 0),".format(**locals()))

    # 2
    print("\n\n\n2) drivers/amlogic/clk/gxbb_hdmi_clk.c: (around line 150)\n")
    print("    VID_CLK({pixel_clock_1000}, {pixel_clock_10000}, 0, 1, DIV_5, 1),".format(**locals()))

    # 3
    print("\n\n\n3) drivers/amlogic/clk/gxbb_hdmi_clk.c: (around line 460)\n")
    print("""    case {pixel_clock_10000}:
        writel(0x580002{pixel_clock_aml_str}, hiu_base + HHI_HDMI_PLL_CNTL);
        writel(0x00000000, hiu_base + HHI_HDMI_PLL_CNTL2);
        writel(0x0d5c5091, hiu_base + HHI_HDMI_PLL_CNTL3);
        writel(0x801da72c, hiu_base + HHI_HDMI_PLL_CNTL4);
        writel(0x71486980, hiu_base + HHI_HDMI_PLL_CNTL5);
        writel(0x00000e55, hiu_base + HHI_HDMI_PLL_CNTL6);
        set_pll(rate_tbl);
        pr_info("hpll reg: 0x%x\\n",
        	readl(hiu_base + HHI_HDMI_PLL_CNTL));
        hdmi_update_bits(HHI_HDMI_PLL_CNTL2, 0xffff, 0x4e00);
        break;""".format(**locals()))

    # 4
    print("\n\n\n4) drivers/amlogic/clk/gxbb_hdmi_clk.c: (around line 760)\n")
    print("        CTS_XXX_TBL({pixel_clock_1000}, {pixel_clock_1000}, 1, 1),".format(**locals()))

    # 5
    print("\n\n\n5) drivers/amlogic/clk/gxbb_hdmi_clk.c: (around line 790)\n")
    print("        CTS_XXX_TBL({pixel_clock_1000}, {pixel_clock_1000}, 1, 1),".format(**locals()))

    # 6
    print("\n\n\n6) drivers/amlogic/display/vout/tv_vout.h: (around line 120)\n")
    print("        {{TVMODE_{width}x{height}p{hz}hz, VMODE_{width}x{height}p{hz}hz}},".format(**locals()))

    # 7
    print("\n\n\n7) drivers/amlogic/display/vout/tv_vout.h: (around line 1080)\n")
    print("""    {
        .name              = "%dx%dp%dhz",
        .mode              = TVMODE_%dx%dp%dhz,
        .width             = %d,
        .height            = %d,
        .field_height      = %d,
        .aspect_ratio_num  = %d,
        .aspect_ratio_den  = %d,
        .sync_duration_num = %d,
        .sync_duration_den = 1,
        .video_clk         = %d,
    },""" % (width, height, hz, width, height, hz, width, height, height, aspect_ratio_num, aspect_ratio_den, hz, pixel_clock_1000000))

    # 8
    print("\n\n\n8) drivers/amlogic/display/vout/tvregs.h: (around line 440)\n")
    print("""static const struct reg_s tvregs_vesa_{width}x{height}_enc[] = {{
    {{MREG_END_MARKER,            0      }}
}};""".format(**locals()))

    # 9
    print("\n\n\n9) drivers/amlogic/hdmi/hdmi_common/hdmi_parameters.c: (around line 1193)\n")
    print("""static struct hdmi_format_para fmt_para_vesa_{width}x{height}p{hz}_{aspect_ratio_num}x{aspect_ratio_den} = {{
    .vic = HDMIV_{width}x{height}p{hz}hz,
    .name = "{width}x{height}p{hz}hz",
    .pixel_repetition_factor = 0,
    .progress_mode = 1,
    .scrambler_en = 0,
    .tmds_clk_div40 = 0,
    .tmds_clk = {pixel_clock_1000},
    .timing = {{
        .pixel_freq = {pixel_clock_1000}, // = (h_total * v_total) / 2
        .h_freq = {h_freq},
        .v_freq = {v_freq},
        .vsync_polarity = {vsync_polarity},
        .hsync_polarity = {hsync_polarity},
        .h_active = {width},
        .h_total = {h_total},
        .h_blank = {h_blank},
        .h_front = {h_front},
        .h_sync = {h_sync},
        .h_back = {h_back},
        .v_active = {height},
        .v_total = {v_total},
        .v_blank = {v_blank},
        .v_front = {v_front},
        .v_sync = {v_sync},
        .v_back = {v_back},
        .v_sync_ln = 1,
    }},
}};""".format(**locals()))

    # 9b
    print("\n\n\n9b) drivers/amlogic/hdmi/hdmi_common/hdmi_parameters.c: (around line 1193)\n")
    print("""        &fmt_para_vesa_{width}x{height}p{hz}_{aspect_ratio_num}x{aspect_ratio_den},""".format(**locals()))

    # 10
    print("\n\n\n10) drivers/amlogic/hdmi/hdmi_tx_20/hdmi_tx_edid.c: (around line 1632)\n")
    print("""        {{"{width}x{height}p{hz}hz", HDMIV_{width}x{height}p{hz}hz}},""".format(**locals()))

    # 11
    print("\n\n\n11) drivers/amlogic/hdmi/hdmi_tx_20/hdmi_tx_main.c: (around line 986)\n")
    print("""        "{width}x{height}p{hz}hz",""".format(**locals()))

    # 12
    print("\n\n\n12) drivers/amlogic/hdmi/hdmi_tx_20/hdmi_tx_video.c: (around line 611)\n")
    print("""    {{
        .VIC		= HDMIV_{width}x{height}p{hz}hz,
        .color_prefer   = COLOR_SPACE_RGB444,
        .color_depth	= hdmi_color_depth_24B,
        .bar_info	= B_BAR_VERT_HORIZ,
        .repeat_time	= NO_REPEAT,
        .aspect_ratio   = TV_ASPECT_RATIO_16_9,
        .cc		= CC_ITU709,
        .ss		= SS_SCAN_UNDER,
        .sc		= SC_SCALE_HORIZ_VERT,
    }},""".format(**locals()))



    P_ENCP_VIDEO_MAX_PXCNT = h_total - 1
    P_ENCP_VIDEO_MAX_LNCNT = v_total - 1
    P_ENCP_VIDEO_HAVON_END = int(mode_line[5]) - 1

    # 13
    print("\n\n\n13) drivers/amlogic/hdmi/hdmi_tx_20/hw/enc_cfg_hw.c: (around line 985)\n")
    print("""static const struct reg_s tvregs_{width}x{height}p{hz}hz[] = {{
    {{P_VENC_VDAC_SETTING, 0xff,}},
    {{P_ENCP_VIDEO_EN, 0,}},
    {{P_ENCI_VIDEO_EN, 0,}},

    {{P_ENCP_VIDEO_MODE, 0x4040,}},
    {{P_ENCP_VIDEO_MODE_ADV, 0x18,}},

    {{P_ENCP_VIDEO_MAX_PXCNT, {P_ENCP_VIDEO_MAX_PXCNT},}},
    {{P_ENCP_VIDEO_MAX_LNCNT, {P_ENCP_VIDEO_MAX_LNCNT},}},
    {{P_ENCP_VIDEO_HAVON_BEGIN, {h_back},}},
    {{P_ENCP_VIDEO_HAVON_END, {P_ENCP_VIDEO_HAVON_END},}},
    {{P_ENCP_VIDEO_VAVON_BLINE, {v_back},}},
    {{P_ENCP_VIDEO_VAVON_ELINE, 1473,}},
    {{P_ENCP_VIDEO_HSO_BEGIN, 0,}},
    {{P_ENCP_VIDEO_HSO_END, {h_sync},}},
    {{P_ENCP_VIDEO_VSO_BEGIN, 0x1E,}},
    {{P_ENCP_VIDEO_VSO_END, 0x32,}},
    {{P_ENCP_VIDEO_VSO_BLINE, 0x0,}},
    {{P_ENCP_VIDEO_VSO_ELINE, {v_sync},}},

    {{P_ENCP_VIDEO_EN, 1,}},
    {{P_ENCI_VIDEO_EN, 0,}},
    {{MREG_END_MARKER, 0}},
}};""".format(**locals()))

    # 14
    print("\n\n\n14) drivers/amlogic/hdmi/hdmi_tx_20/hw/enc_cfg_hw.c: (around line 1032)\n")
    print("""        {{HDMIV_{width}x{height}p{hz}hz, tvregs_{width}x{height}p{hz}hz}},""".format(**locals()))

    # 15
    print("\n\n\n15) drivers/amlogic/hdmi/hdmi_tx_20/hw/hdmi_tx_hw.c: (around line 360)\n")
    print("""        {{HDMIV_{width}x{height}p{hz}hz, 24000, {pixel_clock_10000}, {pixel_clock_1000}, {pixel_clock_1000}, -1, {pixel_clock_1000}}},""".format(**locals()))

    # 16
    print("\n\n\n16) drivers/amlogic/hdmi/hdmi_tx_20/hw/hdmi_tx_hw.c: (around line 1570)\n")
    print("""    case HDMIV_{width}x{height}p{hz}hz:
        INTERLACE_MODE      = 0;
        PIXEL_REPEAT_VENC   = 0;
        PIXEL_REPEAT_HDMI   = 0;
        ACTIVE_PIXELS       = {width};
        ACTIVE_LINES        = {height};
        LINES_F0            = {v_total};
        LINES_F1            = {v_total};
        FRONT_PORCH         = {h_front};
        HSYNC_PIXELS        = {h_sync};
        BACK_PORCH          = {h_back};
        EOF_LINES           = {v_front};
        VSYNC_LINES         = {v_sync};
        SOF_LINES           = {v_back};
        TOTAL_FRAMES        = 4;
        break;""".format(**locals()))

    # 17
    print("\n\n\n17) include/linux/amlogic/hdmi_tx/hdmi_common.h: (around line 187)\n")
    print("""        HDMIV_{width}x{height}p{hz}hz,""".format(**locals()))

    # 18
    print("\n\n\n18) include/linux/amlogic/vout/vinfo.h: (around line 77)\n")
    print("""        VMODE_{width}x{height}p{hz}hz,""".format(**locals()))

    # 19
    print("\n\n\n19) include/linux/amlogic/vout/vinfo.h: (around line 145)\n")
    print("""        TVMODE_{width}x{height}p{hz}hz,""".format(**locals()))
