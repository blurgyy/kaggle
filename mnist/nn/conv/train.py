#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
__author__ = "Blurgy";

import os 
import numpy as np 
import data 
import nn 
import plot 
import click 

import warnings
warnings.filterwarnings("error")

@click.command()
@click.option("--epoch", type = int, default = 10, 
              help = "Specifies number of epoches, 10 by default")
@click.option("--rate", type = float, default = 2e-4, 
              help = "Specifies value of initial learning rate, 2e-4 by default")
@click.option("--decay", type = click.Choice(["exponential", "constant", "linear", "sigmoid", "hyperbola"]), 
              default = "exponential", 
              help = "Specifies decay schedule of learning rate, exponential by default")
@click.option("--continue-at", type = click.Path(exists=True), default = None,
              help = "Continues training at specified file, initializes a new model if not specified")
@click.option("--batch-size", type = int, default = 64,
              help = "Specifies batch size, 64 by default")
def main(epoch, rate, decay, continue_at, batch_size):
    base_learning_rate = rate;
    decay_schedule = nn.decay_schedule(epoch, decay);
    learning_rate = base_learning_rate * decay_schedule;
    if(continue_at and os.path.exists(continue_at)):
        model = data.load_model(continue_at);
    else:
        model = nn.init_model();

    for ep in range(epoch):
        lr = learning_rate[ep];
        train = data.preprocess_training_set();
        print("training set loaded and shuffled");
        X, Y = nn.sample_batches(train, batch_size);
        yes, cnt = 0, 0;
        for i in range(len(X)):
            x, y = X[i], Y[i];
            nn.forward(model, x, is_test_time = False);
            dz, loss = nn.grad(model, y);
            nn.backward(model, dz);

            prediction = np.argmax(model['output'], axis=1);
            score = prediction.reshape(-1,1) == y.reshape(-1,1)
            yes += np.sum(score);
            cnt += len(y);
            print("[%d/%d]: %.2f%%, batch loss = %.2f" % (yes, cnt, yes / cnt * 100, loss), end = '\r');
            nn.update(model, lr);
            # input();
        data.save_model(model);
        print("\nmodel saved\n");

if(__name__ == "__main__"):
    main();