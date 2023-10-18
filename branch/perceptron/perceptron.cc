/*
 * Copyright (c) 2001 University of Texas at Austin
 *
 * Daniel A. Jimenez
 * Calvin Lin
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software (the "Software"), to deal in
 * the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT.  IN NO EVENT SHALL THE UNIVERSITY OF TEXAS AT
 * AUSTIN BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 * IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF
 * OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *
 * This file implements the simulated perceptron branch predictor from:
 *
 * Jimenez, D. A. & Lin, C., Dynamic branch prediction with perceptrons,
 * Proceedings of the Seventh International Symposium on High Performance
 * Computer Architecture (HPCA), Monterrey, NL, Mexico 2001
 *
 * The #define's here specify a perceptron predictor with a history
 * length of 24, 163 perceptrons, and  8-bit weights.  This represents
 * a hardware budget of (24+1)*8*163 = 32600 bits, or about 4K bytes,
 * which is comparable to the hardware budget of the Alpha 21264 hybrid
 * branch predictor.
 */

#include "perceptron.h"
#include "ooo_cpu.h"



void O3_CPU::initialize_branch_predictor() {}

uint8_t O3_CPU::predict_branch(uint64_t ip)
{
  return perceptron_predict(ip, this);
}

void O3_CPU::last_branch_result(uint64_t ip, uint64_t branch_target, uint8_t taken, uint8_t branch_type)
{
  perceptron_train(ip, branch_target, taken, branch_type, this);
}
