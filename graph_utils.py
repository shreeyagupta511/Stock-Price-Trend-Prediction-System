import plotly.graph_objs as go
import plotly.io as pio


# ---------------- LINEAR GRAPH ----------------
def linear_dashboard(x, y, y_pred, next_pred, mae):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=x, y=y,
        mode='markers',
        name='Actual Price'))

    fig.add_trace(
        go.Scatter(x=x, y=y_pred,
        mode='lines',
        name='Linear Fit'))

    fig.add_trace(
        go.Scatter(x=[x[-1] + 1],
        y=[next_pred],
        mode='markers',
        name='Next Day Prediction'))

    fig.update_layout(
    title=f"Linear Regression (MAE: {round(mae,2)})",
    xaxis_title="Time",
    yaxis_title="Price",
    height=400,
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=40, r=20, t=60, b=60))

    return pio.to_html(fig, full_html=False)


# ---------------- EULER GRAPH ----------------
def euler_dashboard(x, y, next_pred, mae):

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x, y=y,
                             mode='markers',
                             name='Actual Price'))

    fig.add_trace(go.Scatter(x=[x[-1] + 1],
                             y=[next_pred],
                             mode='markers',
                             name='Euler Prediction'))

    fig.update_layout(
        title=f"Euler Method (MAE: {round(mae,2)})",
        xaxis_title="Time",
        yaxis_title="Price",
        height=400,
        legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=40, r=20, t=60, b=60))

    return pio.to_html(fig, full_html=False)


# ---------------- DIFFERENTIATION GRAPH ----------------
def diff_dashboard(x, dy):

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x,
        y=dy,
        mode='lines',
        name='Rate of Change'
    ))

    fig.update_layout(
        title="Numerical Differentiation (Momentum)",
        xaxis_title="Time",
        yaxis_title="Rate of Change",
        height=400
    )

    return pio.to_html(fig, full_html=False)

# ---------------- INTERPOLATION GRAPH ----------------
def interpolation_dashboard(x, y, y_pred, next_pred, mae):

    fig = go.Figure()

    # Actual data
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode='markers',
            name='Actual Price'
        )
    )

    # Interpolated curve
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y_pred,
            mode='lines',
            name='Interpolation Curve'
        )
    )

    # Next prediction point
    fig.add_trace(
        go.Scatter(
            x=[x[-1] + 1],
            y=[next_pred],
            mode='markers',
            name='Next Day Prediction'
        )
    )

    fig.update_layout(
        title=f"Interpolation Method (MAE: {round(mae,2)})",
        xaxis_title="Time",
        yaxis_title="Price",
        height=400,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=40, r=20, t=60, b=60)
    )

    return pio.to_html(fig, full_html=False)