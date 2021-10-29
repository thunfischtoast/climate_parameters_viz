import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib


def main():

    # read climate_parameters.xlxs into dataframe
    df = pd.read_csv("climate_parameters.csv")

    # fill missing values with last available data
    df = df.fillna(method="ffill")

    # normalize columns to [0,1]
    df_rel = df - df.min()
    df_rel = df_rel.div(df_rel.max(), axis=1)
    df_rel["Year"] = df["Year"]

    plt.close()
    plt.rcParams["figure.autolayout"] = True
    plt.rcParams["figure.figsize"] = (10, 7.5)

    sns.set_style("white")

    def animate(i):
        print(i)
        plt.clf()
        data = df_rel.iloc[0:i]

        # create a seaborn lineplot
        ax = sns.lineplot(x="Year", y="Atmosphere CO2 concentration (ppm)", data=data)

        # add other lines
        for col in data:
            if col not in ["Year", "Atmosphere CO2 concentration (ppm)"]:
                sns.lineplot(x="Year", y=data[col], data=data, ax=ax)

        ax.set_xlim(df_rel["Year"].min(), df_rel["Year"].max())
        ax.set_ylim(0, 1)
        ax.set(xlabel="Year", ylabel=None, yticklabels=[])

        sns.despine(ax=ax, top=True, right=True, left=True, bottom=False)
        ax.tick_params(left=False)  # remove the ticks

        # set title
        ax.set_title(
            "Various climate parameters\nScaled between min and max of 1900 - 2020"
        )

        # add a legend

        ax.legend(labels=[col for col in data if col != "Year"], loc="upper left")

        ax.text(
            0.75,
            0.2,
            "Year: " + str(int(df.iloc[i]["Year"])),
            horizontalalignment="left",
            verticalalignment="bottom",
            transform=ax.transAxes,
        )
        ax.text(
            0.75,
            0.16,
            "CO2 concentration: "
            + str(int(df.iloc[i]["Atmosphere CO2 concentration (ppm)"]))
            + " ppm",
            horizontalalignment="left",
            verticalalignment="bottom",
            transform=ax.transAxes,
            color="#4c72b0",
        )
        ax.text(
            0.75,
            0.12,
            "Fossil fuel emissions running total: "
            + str(
                int(
                    df.iloc[i][
                        "Running total human fossil fuel + cement production CO2 emissions (million metric tons of CO2) since 1750"
                    ]
                )
            )
            + " M ton CO2",
            horizontalalignment="left",
            verticalalignment="bottom",
            transform=ax.transAxes,
            color="#dd8452",
        )
        ax.text(
            0.75,
            0.08,
            "Sea level change: "
            + str(int(df.iloc[i]["Global average sea level change since 1900 (mm)"]))
            + " mm",
            horizontalalignment="left",
            verticalalignment="bottom",
            transform=ax.transAxes,
            color="#55a868",
        )
        ax.text(
            0.75,
            0.04,
            "Global temperature change: "
            + str(
                round(
                    df.iloc[i][
                        "Global Annual Temperature Anomaly compared to 1900 (°C)"
                    ],
                    2,
                )
            )
            + " °C",
            horizontalalignment="left",
            verticalalignment="bottom",
            transform=ax.transAxes,
            color="#c44e52",
        )

    fig = plt.figure()
    # animate the plot along x-axis
    animate(len(df_rel) - 1)

    # plt.show()
    plt.savefig("climate_parameters.png", dpi=300)

    plt.clf()
    anim = matplotlib.animation.FuncAnimation(
        fig=fig, func=animate, frames=len(df_rel), interval=100, repeat=False
    )

    anim.save("climate_parameters.gif", writer="imagemagick", fps=10)
    # show the plot
    # plt.show()


if __name__ == "__main__":
    main()
