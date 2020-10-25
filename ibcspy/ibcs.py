import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import numpy as np
from colormap import rgb2hex

class Ibcs():
    def ibcs_grid(self,fig
              ,major_ticks1
            ,major_ticks2
            ,perc_ticks
            ,m_gr
            ,t_gr
            ,l_gr
            ,offset
            ,**kwargs):
        """Creates a Gridspec for subplots
        
        Arguments:
            fig {[type]} -- Matplotlib figure
            major_ticks1 {[type]} -- y-axis ticks for the major plot
            major_ticks2 {[type]} -- y-axis ticks for the delta plot
            perc_ticks {[type]} -- y-axis ticks for the percentage delta plot
            m_gr {[type]} -- gridspec size for message
            t_gr {[type]} -- gridspec size for title 
            l_gr {[type]} -- space padding top
            offset {[type]} -- space padding bottom
        
        Returns:
            [type] -- [description]
        """
        # Define Gridspec and Sub-Grids
        col = 1
        row = m_gr+t_gr + l_gr+(len(perc_ticks) + len(major_ticks1) + len(major_ticks2))+offset
        gs = gridspec.GridSpec(ncols =col,nrows=row)

        s0col = 1
        s0row = m_gr+t_gr 
        loc_0 = (m_gr+t_gr)
        gs0 = gridspec.GridSpecFromSubplotSpec(nrows=s0row,ncols = s0col, subplot_spec=gs[:loc_0])

        s1col = 1
        s1row = (len(perc_ticks) + len(major_ticks1) + len(major_ticks2))
        gs1 = gridspec.GridSpecFromSubplotSpec(nrows = s1row, ncols=s1col, subplot_spec=gs[loc_0:])

        msg = fig.add_subplot(gs0[:m_gr, 0])
        tit = fig.add_subplot(gs0[m_gr:, 0])

        ax0 = fig.add_subplot(gs1[l_gr:(l_gr+len(perc_ticks)), 0])  
        ax1 = fig.add_subplot(gs1[(l_gr+len(perc_ticks)):(l_gr+(len(perc_ticks) + len(major_ticks2))), 0], sharex=ax0)
        ax2 = fig.add_subplot(gs1[(l_gr+(len(perc_ticks) + len(major_ticks2))):(l_gr+(len(perc_ticks) + len(major_ticks1) + len(major_ticks2))), 0], sharex=ax0)

        return ax0, ax1, ax2, msg, tit

    def remove_borders(self,x, dates, ax0, ax1, ax2, msg, tit):
        """Remove borders from plot

        Arguments:
            x {[type]} -- [description]
            dates {[type]} -- [description]
            ax0 {[type]} -- [description]
            ax1 {[type]} -- [description]
            ax2 {[type]} -- [description]
            msg {[type]} -- [description]
            tit {[type]} -- [description]
        """
        ax1.set_xticks(x);
        ax2.set_xticks(x);

        # Remove Frame
        ax0.set_frame_on(False)
        ax2.set_frame_on(False)
        ax1.set_frame_on(False)
        msg.set_frame_on(False)
        tit.spines['bottom'].set_visible(False)
        tit.spines['right'].set_visible(False)
        tit.spines['left'].set_visible(False) 

        # Remove Ticks   
        ax2.set_xticks(x)
        ax2.set_xticklabels(dates);

        ax0.tick_params(axis='both', which='both', length=0)
        ax1.tick_params(axis='both', which='both', length=0)
        ax2.tick_params(axis='both', which='both', length=0)
        msg.tick_params(axis='both', which='both', length=0)
        tit.tick_params(axis='both', which='both', length=0)

        plt.setp(ax0.get_xticklabels(), visible=False)
        plt.setp(ax1.get_xticklabels(), visible=False)
        plt.setp(msg.get_xticklabels(), visible=False)
        plt.setp(tit.get_xticklabels(), visible=False)

        plt.setp(ax0.get_yticklabels(), visible=False)
        plt.setp(ax1.get_yticklabels(), visible=False)
        plt.setp(ax2.get_yticklabels(), visible=False)
        plt.setp(msg.get_yticklabels(), visible=False)
        plt.setp(tit.get_yticklabels(), visible=False)    

    def ibcs_barchart(self,
        data
        ,dates
        ,**kwargs
    ):

        x = np.arange(data.shape[1])
        delta = data[1] - data[0]
        delta_perc = delta / data[0]
        idx_pos = (delta > 0)
        major_ticks1 = np.arange(data.max(),data.min(),-5)
        major_ticks2 = np.arange(delta.max(),delta.min(),-5)
        perc_ticks = np.arange(np.ceil(np.nanmin([delta_perc.max(),kwargs['cap_perc']])*10)/10,np.floor(delta_perc.min()*10)/10,-0.1)

        fig = plt.figure()
        m_gr = kwargs['m_gr']
        t_gr = kwargs['t_gr']
        l_gr = kwargs['l_gr']
        offset = kwargs['offset']
        axis_pad = kwargs['axis_pad']
        
        ax0, ax1, ax2, msg, tit = self.ibcs_grid(fig,
            major_ticks1
            ,major_ticks2
            ,perc_ticks
            ,m_gr
            ,t_gr
            ,l_gr
            ,offset
            )

        # Remove Plot Borders
        ax1.set_ylim(major_ticks2[-1]-axis_pad,major_ticks2[0]+axis_pad)
        ax2.set_ylim(major_ticks1[-1]-axis_pad,major_ticks1[0]+axis_pad)

        self.remove_borders(x, dates, ax0, ax1, ax2, msg, tit)

        msg.text(0, 1, "Message", size=10);
        tit.text(0, 0, "SomeG GmbH\n"+r"$\bf{Revenue}$"+" in mEUR\nPY, CY 2009..2018", size=10);

        # Plots
        ax0.plot(x,np.zeros(len(x)),color=rgb2hex(0, 0, 0),linewidth=2)
        ax0.scatter(x,delta_perc,marker='s',color=rgb2hex(0, 0, 0))
        ax0.bar(x[idx_pos],delta_perc[idx_pos],color=rgb2hex(140, 180, 0),width=0.05)
        ax0.bar(x[~idx_pos],delta_perc[~idx_pos],color=rgb2hex(250, 0, 0),width=0.05)

        ax1.plot(x,np.zeros(len(x)),color='k',linewidth=2)
        ax1.bar(x[idx_pos],delta[idx_pos],color=rgb2hex(140, 180, 0),width=0.5)
        ax1.bar(x[~idx_pos],delta[~idx_pos],color=rgb2hex(250, 0, 0),width=0.5)

        ax2.plot(x,np.zeros(len(x))+1,color='k',linewidth=1)
        ax2.bar(x - 0.5/9, data[0], color = rgb2hex(255, 255, 255), width = 0.5,edgecolor=['k'])
        ax2.bar(x + 0, data[1], color = rgb2hex(64, 64, 64), width = 0.5)

        for ix in x:
            if ix in x[idx_pos]:
                va = 'bottom'
                space = kwargs['label_space']
            else:
                va = 'top'
                space = -kwargs['label_space']
            label = '{0:+}'.format(int(delta_perc[ix]*100))

            ax0.annotate(
                        label,                      # Use `label` as label
                        (x[ix], delta_perc[ix]),         # Place label at end of the bar
                        xytext=(0, space*3),          # Vertically shift label by `space`
                        textcoords="offset points", # Interpret `xytext` as offset in points
                        ha='center',                # Horizontally center label
                        va=va)                      # Vertically align label differently for
            label = '{0:+}'.format(int(round(delta[ix]/kwargs['label_normalize'],0)))
            ax1.annotate(
                        label,                      # Use `label` as label
                        (x[ix], delta[ix]),         # Place label at end of the bar
                        xytext=(0, space),          # Vertically shift label by `space`
                        textcoords="offset points", # Interpret `xytext` as offset in points
                        ha='center',                # Horizontally center label
                        va=va)                      # Vertically align label differently for
                                                    # positive and negative values.                                                   # positive and negative values.    

        ax0.text(-0.5,0,'\u0394BU %')
        ax1.text(-0.5,0,'\u0394BU')    

        for ix in range(len(x)):
            if data[1][ix] > 0:
                va = 'bottom'
                space = kwargs['label_space']
            else:
                va = 'top'
                space = -kwargs['label_space']     
            label = str(int(round(data[1][ix]/kwargs['label_normalize'],1)))
            ax2.annotate(
                        label,                      # Use `label` as label
                        (x[ix], data[1][ix]),         # Place label at end of the bar
                        xytext=(0, space),          # Vertically shift label by `space`
                        textcoords="offset points", # Interpret `xytext` as offset in points
                        ha='center',                # Horizontally center label
                        va=va)                      # Vertically align label differently for
                                                    # positive and negative values.
        return plt.show()