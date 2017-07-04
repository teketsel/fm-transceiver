#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: TGS FM Transciever
# Author: Boyan Naydenov
# Generated: Thu Jun 15 12:12:50 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import gpredict
import sip
import sys
import time


class fm_transciever(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "TGS FM Transciever")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("TGS FM Transciever")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "fm_transciever")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.rx_center_freq = rx_center_freq = 100e6
        self.doppler_freq = doppler_freq = rx_center_freq
        self.tx_ptt = tx_ptt = 1
        self.tx_gain = tx_gain = 30
        self.tx_freq = tx_freq = 100e6
        self.samp_rate = samp_rate = 250e3
        self.rx_switch = rx_switch = 1
        self.rx_mode = rx_mode = 1
        self.rx_gain = rx_gain = 30
        self.doppler_shift = doppler_shift = int(doppler_freq-rx_center_freq)
        self.doppler_mode = doppler_mode = 0
        self.audio_rate = audio_rate = 48e3
        self.audio_interp = audio_interp = 4

        ##################################################
        # Blocks
        ##################################################
        self.wrapper = Qt.QTabWidget()
        self.wrapper_widget_0 = Qt.QWidget()
        self.wrapper_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.wrapper_widget_0)
        self.wrapper_grid_layout_0 = Qt.QGridLayout()
        self.wrapper_layout_0.addLayout(self.wrapper_grid_layout_0)
        self.wrapper.addTab(self.wrapper_widget_0, 'RX')
        self.wrapper_widget_1 = Qt.QWidget()
        self.wrapper_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.wrapper_widget_1)
        self.wrapper_grid_layout_1 = Qt.QGridLayout()
        self.wrapper_layout_1.addLayout(self.wrapper_grid_layout_1)
        self.wrapper.addTab(self.wrapper_widget_1, 'TX')
        self.top_layout.addWidget(self.wrapper)
        _tx_ptt_push_button = Qt.QPushButton('PTT')
        self._tx_ptt_choices = {'Pressed': 0, 'Released': 1}
        _tx_ptt_push_button.pressed.connect(lambda: self.set_tx_ptt(self._tx_ptt_choices['Pressed']))
        _tx_ptt_push_button.released.connect(lambda: self.set_tx_ptt(self._tx_ptt_choices['Released']))
        self.wrapper_grid_layout_1.addWidget(_tx_ptt_push_button, 1,0,1,4)
        self._tx_gain_range = Range(0, 90, 1, 30, 200)
        self._tx_gain_win = RangeWidget(self._tx_gain_range, self.set_tx_gain, 'TX Gain', "counter_slider", float)
        self.wrapper_grid_layout_1.addWidget(self._tx_gain_win, 0,2,1,2)
        self._tx_freq_tool_bar = Qt.QToolBar(self)
        self._tx_freq_tool_bar.addWidget(Qt.QLabel('TX Freq'+": "))
        self._tx_freq_line_edit = Qt.QLineEdit(str(self.tx_freq))
        self._tx_freq_tool_bar.addWidget(self._tx_freq_line_edit)
        self._tx_freq_line_edit.returnPressed.connect(
        	lambda: self.set_tx_freq(eng_notation.str_to_num(str(self._tx_freq_line_edit.text().toAscii()))))
        self.wrapper_grid_layout_1.addWidget(self._tx_freq_tool_bar, 0,0,1,2)
        _rx_switch_check_box = Qt.QCheckBox('RX Switch')
        self._rx_switch_choices = {True: 0, False: 1}
        self._rx_switch_choices_inv = dict((v,k) for k,v in self._rx_switch_choices.iteritems())
        self._rx_switch_callback = lambda i: Qt.QMetaObject.invokeMethod(_rx_switch_check_box, "setChecked", Qt.Q_ARG("bool", self._rx_switch_choices_inv[i]))
        self._rx_switch_callback(self.rx_switch)
        _rx_switch_check_box.stateChanged.connect(lambda i: self.set_rx_switch(self._rx_switch_choices[bool(i)]))
        self.wrapper_grid_layout_0.addWidget(_rx_switch_check_box, 1,0,1,2)
        self._rx_mode_options = (0, 1, )
        self._rx_mode_labels = ('NBFM RX', 'WBFM RX', )
        self._rx_mode_tool_bar = Qt.QToolBar(self)
        self._rx_mode_tool_bar.addWidget(Qt.QLabel('RX Mode'+": "))
        self._rx_mode_combo_box = Qt.QComboBox()
        self._rx_mode_tool_bar.addWidget(self._rx_mode_combo_box)
        for label in self._rx_mode_labels: self._rx_mode_combo_box.addItem(label)
        self._rx_mode_callback = lambda i: Qt.QMetaObject.invokeMethod(self._rx_mode_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._rx_mode_options.index(i)))
        self._rx_mode_callback(self.rx_mode)
        self._rx_mode_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_rx_mode(self._rx_mode_options[i]))
        self.wrapper_grid_layout_0.addWidget(self._rx_mode_tool_bar, 1,2,1,2)
        self._rx_gain_range = Range(0, 90, 1, 30, 200)
        self._rx_gain_win = RangeWidget(self._rx_gain_range, self.set_rx_gain, 'RX gain', "counter_slider", float)
        self.wrapper_grid_layout_0.addWidget(self._rx_gain_win, 0,2,1,2)
        self._rx_center_freq_tool_bar = Qt.QToolBar(self)
        self._rx_center_freq_tool_bar.addWidget(Qt.QLabel('RX Freq'+": "))
        self._rx_center_freq_line_edit = Qt.QLineEdit(str(self.rx_center_freq))
        self._rx_center_freq_tool_bar.addWidget(self._rx_center_freq_line_edit)
        self._rx_center_freq_line_edit.returnPressed.connect(
        	lambda: self.set_rx_center_freq(eng_notation.str_to_num(str(self._rx_center_freq_line_edit.text().toAscii()))))
        self.wrapper_grid_layout_0.addWidget(self._rx_center_freq_tool_bar, 0,0,1,2)
        self._doppler_shift_tool_bar = Qt.QToolBar(self)
        
        if None:
          self._doppler_shift_formatter = None
        else:
          self._doppler_shift_formatter = lambda x: x
        
        self._doppler_shift_tool_bar.addWidget(Qt.QLabel('Doppler Shift'+": "))
        self._doppler_shift_label = Qt.QLabel(str(self._doppler_shift_formatter(self.doppler_shift)))
        self._doppler_shift_tool_bar.addWidget(self._doppler_shift_label)
        self.top_layout.addWidget(self._doppler_shift_tool_bar)
          
        _doppler_mode_check_box = Qt.QCheckBox('Doppler correction')
        self._doppler_mode_choices = {True: 1, False: 0}
        self._doppler_mode_choices_inv = dict((v,k) for k,v in self._doppler_mode_choices.iteritems())
        self._doppler_mode_callback = lambda i: Qt.QMetaObject.invokeMethod(_doppler_mode_check_box, "setChecked", Qt.Q_ARG("bool", self._doppler_mode_choices_inv[i]))
        self._doppler_mode_callback(self.doppler_mode)
        _doppler_mode_check_box.stateChanged.connect(lambda i: self.set_doppler_mode(self._doppler_mode_choices[bool(i)]))
        self.top_layout.addWidget(_doppler_mode_check_box)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(rx_center_freq, 0)
        self.uhd_usrp_source_0.set_gain(rx_gain, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(tx_freq, 0)
        self.uhd_usrp_sink_0.set_gain(tx_gain, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=int(samp_rate),
                decimation=int(audio_interp*audio_rate),
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=int(audio_rate*audio_interp),
                decimation=int(samp_rate),
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_waterfall_sink_x_0_0 = qtgui.waterfall_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"RX Waterfall", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0_0.enable_axis_labels(True)
        
        if not True:
          self.qtgui_waterfall_sink_x_0_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0_0.set_plot_pos_half(not True)
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_0.set_line_alpha(i, alphas[i])
        
        self.qtgui_waterfall_sink_x_0_0.set_intensity_range(-140, 10)
        
        self._qtgui_waterfall_sink_x_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.wrapper_grid_layout_0.addWidget(self._qtgui_waterfall_sink_x_0_0_win, 2,2,1,2)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"TX Waterfall", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)
        
        if not True:
          self.qtgui_waterfall_sink_x_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0.set_plot_pos_half(not True)
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])
        
        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)
        
        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.wrapper_grid_layout_1.addWidget(self._qtgui_waterfall_sink_x_0_win, 2,2,1,2)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"RX FFT", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0_0.enable_grid(True)
        self.qtgui_freq_sink_x_0_0.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_freq_sink_x_0_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0_0.set_plot_pos_half(not True)
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.wrapper_grid_layout_0.addWidget(self._qtgui_freq_sink_x_0_0_win, 2,0,1,2)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"TX  FFT", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.wrapper_grid_layout_1.addWidget(self._qtgui_freq_sink_x_0_win, 2,0,1,2)
        self.gpredict_doppler_0_0 = gpredict.doppler(self.set_doppler_freq, "localhost", 4532, True)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blks2_valve_0_0 = grc_blks2.valve(item_size=gr.sizeof_gr_complex*1, open=bool(rx_switch))
        self.blks2_valve_0 = grc_blks2.valve(item_size=gr.sizeof_float*1, open=bool(tx_ptt))
        self.blks2_selector_1_0 = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*1,
        	num_inputs=2,
        	num_outputs=1,
        	input_index=doppler_mode,
        	output_index=0,
        )
        self.blks2_selector_1 = grc_blks2.selector(
        	item_size=gr.sizeof_float*1,
        	num_inputs=2,
        	num_outputs=1,
        	input_index=rx_mode,
        	output_index=0,
        )
        self.blks2_selector_0 = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*1,
        	num_inputs=1,
        	num_outputs=2,
        	input_index=0,
        	output_index=rx_mode,
        )
        self.audio_source_0 = audio.source(int(audio_rate), '', True)
        self.audio_sink_0 = audio.sink(int(audio_rate), '', True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=audio_interp*audio_rate,
        	audio_decimation=audio_interp,
        )
        self.analog_sig_source_x_1 = analog.sig_source_c(int(audio_rate*audio_interp), analog.GR_COS_WAVE, doppler_shift, 1, 0)
        self.analog_nbfm_tx_0 = analog.nbfm_tx(
        	audio_rate=int(audio_rate),
        	quad_rate=int(audio_rate*audio_interp),
        	tau=75e-6,
        	max_dev=5e3,
        	fh=-1.0,
                )
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=int(audio_rate),
        	quad_rate=int(audio_rate*audio_interp),
        	tau=75e-6,
        	max_dev=5e3,
          )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_nbfm_rx_0, 0), (self.blks2_selector_1, 0))    
        self.connect((self.analog_nbfm_tx_0, 0), (self.rational_resampler_xxx_1, 0))    
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.analog_wfm_rcv_0, 0), (self.blks2_selector_1, 1))    
        self.connect((self.audio_source_0, 0), (self.blks2_valve_0, 0))    
        self.connect((self.blks2_selector_0, 0), (self.analog_nbfm_rx_0, 0))    
        self.connect((self.blks2_selector_0, 1), (self.analog_wfm_rcv_0, 0))    
        self.connect((self.blks2_selector_1, 0), (self.audio_sink_0, 0))    
        self.connect((self.blks2_selector_1_0, 0), (self.blks2_selector_0, 0))    
        self.connect((self.blks2_valve_0, 0), (self.analog_nbfm_tx_0, 0))    
        self.connect((self.blks2_valve_0_0, 0), (self.qtgui_freq_sink_x_0_0, 0))    
        self.connect((self.blks2_valve_0_0, 0), (self.qtgui_waterfall_sink_x_0_0, 0))    
        self.connect((self.blks2_valve_0_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.blks2_selector_1_0, 1))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.blks2_selector_1_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.rational_resampler_xxx_1, 0), (self.qtgui_freq_sink_x_0, 0))    
        self.connect((self.rational_resampler_xxx_1, 0), (self.qtgui_waterfall_sink_x_0, 0))    
        self.connect((self.rational_resampler_xxx_1, 0), (self.uhd_usrp_sink_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.blks2_valve_0_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "fm_transciever")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_rx_center_freq(self):
        return self.rx_center_freq

    def set_rx_center_freq(self, rx_center_freq):
        self.rx_center_freq = rx_center_freq
        Qt.QMetaObject.invokeMethod(self._rx_center_freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.rx_center_freq)))
        self.set_doppler_shift(self._doppler_shift_formatter(int(self.doppler_freq-self.rx_center_freq)))
        self.uhd_usrp_source_0.set_center_freq(self.rx_center_freq, 0)
        self.set_doppler_freq(self.rx_center_freq)

    def get_doppler_freq(self):
        return self.doppler_freq

    def set_doppler_freq(self, doppler_freq):
        self.doppler_freq = doppler_freq
        self.set_doppler_shift(self._doppler_shift_formatter(int(self.doppler_freq-self.rx_center_freq)))

    def get_tx_ptt(self):
        return self.tx_ptt

    def set_tx_ptt(self, tx_ptt):
        self.tx_ptt = tx_ptt
        self.blks2_valve_0.set_open(bool(self.tx_ptt))

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.uhd_usrp_sink_0.set_gain(self.tx_gain, 0)
        	

    def get_tx_freq(self):
        return self.tx_freq

    def set_tx_freq(self, tx_freq):
        self.tx_freq = tx_freq
        Qt.QMetaObject.invokeMethod(self._tx_freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.tx_freq)))
        self.uhd_usrp_sink_0.set_center_freq(self.tx_freq, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.qtgui_waterfall_sink_x_0_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_rx_switch(self):
        return self.rx_switch

    def set_rx_switch(self, rx_switch):
        self.rx_switch = rx_switch
        self._rx_switch_callback(self.rx_switch)
        self.blks2_valve_0_0.set_open(bool(self.rx_switch))

    def get_rx_mode(self):
        return self.rx_mode

    def set_rx_mode(self, rx_mode):
        self.rx_mode = rx_mode
        self._rx_mode_callback(self.rx_mode)
        self.blks2_selector_1.set_input_index(int(self.rx_mode))
        self.blks2_selector_0.set_output_index(int(self.rx_mode))

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.uhd_usrp_source_0.set_gain(self.rx_gain, 0)
        	

    def get_doppler_shift(self):
        return self.doppler_shift

    def set_doppler_shift(self, doppler_shift):
        self.doppler_shift = doppler_shift
        Qt.QMetaObject.invokeMethod(self._doppler_shift_label, "setText", Qt.Q_ARG("QString", str(self.doppler_shift)))
        self.analog_sig_source_x_1.set_frequency(self.doppler_shift)

    def get_doppler_mode(self):
        return self.doppler_mode

    def set_doppler_mode(self, doppler_mode):
        self.doppler_mode = doppler_mode
        self._doppler_mode_callback(self.doppler_mode)
        self.blks2_selector_1_0.set_input_index(int(self.doppler_mode))

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.analog_sig_source_x_1.set_sampling_freq(int(self.audio_rate*self.audio_interp))

    def get_audio_interp(self):
        return self.audio_interp

    def set_audio_interp(self, audio_interp):
        self.audio_interp = audio_interp
        self.analog_sig_source_x_1.set_sampling_freq(int(self.audio_rate*self.audio_interp))


def main(top_block_cls=fm_transciever, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
