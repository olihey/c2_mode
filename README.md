# c2_mode
A Python script to help create new view modes for the ODROID-C2

## Usage
```
python3.5 c2_mode.py <Modeline_string>
```

## Example
```
$ python3.5 c2_mode.py Modeline "2560x1440_60.00"  311.83  2560 2744 3024 3488  1440 1441 1444 1490  -HSync +Vsync
['Modeline', '2560x1440_60.00', '311.83', '2560', '2744', '3024', '3488', '1440', '1441', '1444', '1490', '-HSync', '+Vsync']



1) drivers/amlogic/clk/gxbb_hdmi_clk.c: (around line 125)

    HPLL_FVCO_RATE(3118300, 0x40, 0x1, 0, 0),



2) drivers/amlogic/clk/gxbb_hdmi_clk.c: (around line 150)

    VID_CLK(311830, 3118300, 0, 1, DIV_5, 1),



3) drivers/amlogic/clk/gxbb_hdmi_clk.c: (around line 460)

    case 3118300:
        writel(0x58000240, hiu_base + HHI_HDMI_PLL_CNTL);
        writel(0x00000000, hiu_base + HHI_HDMI_PLL_CNTL2);
        writel(0x0d5c5091, hiu_base + HHI_HDMI_PLL_CNTL3);
        writel(0x801da72c, hiu_base + HHI_HDMI_PLL_CNTL4);
        writel(0x71486980, hiu_base + HHI_HDMI_PLL_CNTL5);
        writel(0x00000e55, hiu_base + HHI_HDMI_PLL_CNTL6);
        set_pll(rate_tbl);
        pr_info("hpll reg: 0x%x\n",
        	readl(hiu_base + HHI_HDMI_PLL_CNTL));
        hdmi_update_bits(HHI_HDMI_PLL_CNTL2, 0xffff, 0x4e00);
        break;



4) drivers/amlogic/clk/gxbb_hdmi_clk.c: (around line 760)

        CTS_XXX_TBL(311830, 311830, 1, 1),



5) drivers/amlogic/clk/gxbb_hdmi_clk.c: (around line 790)

        CTS_XXX_TBL(311830, 311830, 1, 1),



6) drivers/amlogic/display/vout/tv_vout.h: (around line 120)

        {TVMODE_2560x1440p60hz, VMODE_2560x1440p60hz},



7) drivers/amlogic/display/vout/tv_vout.h: (around line 1080)

    {
        .name              = "2560x1440p60hz",
        .mode              = TVMODE_2560x1440p60hz,
        .width             = 2560,
        .height            = 1440,
        .field_height      = 1440,
        .aspect_ratio_num  = 16,
        .aspect_ratio_den  = 9,
        .sync_duration_num = 60,
        .sync_duration_den = 1,
        .video_clk         = 311830000,
    },



8) drivers/amlogic/display/vout/tvregs.h: (around line 440)

static const struct reg_s tvregs_vesa_2560x1440_enc[] = {
    {MREG_END_MARKER,            0      }
};



9) drivers/amlogic/hdmi/hdmi_common/hdmi_parameters.c: (around line 1193)

static struct hdmi_format_para fmt_para_vesa_2560x1440p60_16x9 = {
    .vic = HDMIV_2560x1440p60hz,
    .name = "2560x1440p60hz",
    .pixel_repetition_factor = 0,
    .progress_mode = 1,
    .scrambler_en = 0,
    .tmds_clk_div40 = 0,
    .tmds_clk = 311830,
    .timing = {
        .pixel_freq = 311830, // = (h_total * v_total) / 2
        .h_freq = 89340,
        .v_freq = 60000,
        .vsync_polarity = 1,
        .hsync_polarity = 0,
        .h_active = 2560,
        .h_total = 3488,
        .h_blank = 928,
        .h_front = 184,
        .h_sync = 280,
        .h_back = 464,
        .v_active = 1440,
        .v_total = 1490,
        .v_blank = 50,
        .v_front = 1,
        .v_sync = 3,
        .v_back = 46,
        .v_sync_ln = 1,
    },
};



9b) drivers/amlogic/hdmi/hdmi_common/hdmi_parameters.c: (around line 1193)

        &fmt_para_vesa_2560x1440p60_16x9,



10) drivers/amlogic/hdmi/hdmi_tx_20/hdmi_tx_edid.c: (around line 1632)

        {"2560x1440p60hz", HDMIV_2560x1440p60hz},



11) drivers/amlogic/hdmi/hdmi_tx_20/hdmi_tx_main.c: (around line 986)

        "2560x1440p60hz",



12) drivers/amlogic/hdmi/hdmi_tx_20/hdmi_tx_video.c: (around line 611)

    {
        .VIC		= HDMIV_2560x1440p60hz,
        .color_prefer   = COLOR_SPACE_RGB444,
        .color_depth	= hdmi_color_depth_24B,
        .bar_info	= B_BAR_VERT_HORIZ,
        .repeat_time	= NO_REPEAT,
        .aspect_ratio   = TV_ASPECT_RATIO_16_9,
        .cc		= CC_ITU709,
        .ss		= SS_SCAN_UNDER,
        .sc		= SC_SCALE_HORIZ_VERT,
    },



13) drivers/amlogic/hdmi/hdmi_tx_20/hw/enc_cfg_hw.c: (around line 985)

static const struct reg_s tvregs_2560x1440p60hz[] = {
    {P_VENC_VDAC_SETTING, 0xff,},
    {P_ENCP_VIDEO_EN, 0,},
    {P_ENCI_VIDEO_EN, 0,},

    {P_ENCP_VIDEO_MODE, 0x4040,},
    {P_ENCP_VIDEO_MODE_ADV, 0x18,},

    {P_ENCP_VIDEO_MAX_PXCNT, 3487,},
    {P_ENCP_VIDEO_MAX_LNCNT, 1489,},
    {P_ENCP_VIDEO_HAVON_BEGIN, 464,},
    {P_ENCP_VIDEO_HAVON_END, 3023,},
    {P_ENCP_VIDEO_VAVON_BLINE, 46,},
    {P_ENCP_VIDEO_VAVON_ELINE, 1473,},
    {P_ENCP_VIDEO_HSO_BEGIN, 0,},
    {P_ENCP_VIDEO_HSO_END, 280,},
    {P_ENCP_VIDEO_VSO_BEGIN, 0x1E,},
    {P_ENCP_VIDEO_VSO_END, 0x32,},
    {P_ENCP_VIDEO_VSO_BLINE, 0x0,},
    {P_ENCP_VIDEO_VSO_ELINE, 3,},

    {P_ENCP_VIDEO_EN, 1,},
    {P_ENCI_VIDEO_EN, 0,},
    {MREG_END_MARKER, 0},
};



14) drivers/amlogic/hdmi/hdmi_tx_20/hw/enc_cfg_hw.c: (around line 1032)

        {HDMIV_2560x1440p60hz, tvregs_2560x1440p60hz},



15) drivers/amlogic/hdmi/hdmi_tx_20/hw/hdmi_tx_hw.c: (around line 360)

        {HDMIV_2560x1440p60hz, 24000, 3118300, 311830, 311830, -1, 311830},



16) drivers/amlogic/hdmi/hdmi_tx_20/hw/hdmi_tx_hw.c: (around line 1570)

    case HDMIV_2560x1440p60hz:
        INTERLACE_MODE      = 0;
        PIXEL_REPEAT_VENC   = 0;
        PIXEL_REPEAT_HDMI   = 0;
        ACTIVE_PIXELS       = 2560;
        ACTIVE_LINES        = 1440;
        LINES_F0            = 1490;
        LINES_F1            = 1490;
        FRONT_PORCH         = 184;
        HSYNC_PIXELS        = 280;
        BACK_PORCH          = 464;
        EOF_LINES           = 1;
        VSYNC_LINES         = 3;
        SOF_LINES           = 46;
        TOTAL_FRAMES        = 4;
        break;



17) include/linux/amlogic/hdmi_tx/hdmi_common.h: (around line 187)

        HDMIV_2560x1440p60hz,



18) include/linux/amlogic/vout/vinfo.h: (around line 77)

        VMODE_2560x1440p60hz,



19) include/linux/amlogic/vout/vinfo.h: (around line 145)

        TVMODE_2560x1440p60hz,
```
