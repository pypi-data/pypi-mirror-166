#pragma once

#include "algorithms/synthesis/syrec_synthesis.hpp"

namespace syrec {
    class SyrecSynthesisAdditionalLines: public SyrecSynthesis {
    public:
        using SyrecSynthesis::SyrecSynthesis;

        static bool synthesize(circuit& circ, const program& program, const properties::ptr& settings = std::make_shared<properties>(), const properties::ptr& statistics = std::make_shared<properties>());

    protected:
        bool process_statement(const statement::ptr& statement) override {
            return !SyrecSynthesis::on_statement(statement);
        }

        void assign_add(bool& status, std::vector<unsigned>& lhs, std::vector<unsigned>& rhs, [[maybe_unused]] const unsigned& op) override {
            status = SyrecSynthesis::increase(lhs, rhs);
        }

        void assign_subtract(bool& status, std::vector<unsigned>& lhs, std::vector<unsigned>& rhs, [[maybe_unused]] const unsigned& op) override {
            status = SyrecSynthesis::decrease(lhs, rhs);
        }

        void assign_exor(bool& status, std::vector<unsigned>& lhs, std::vector<unsigned>& rhs, [[maybe_unused]] const unsigned& op) override {
            status = SyrecSynthesis::bitwise_cnot(lhs, rhs);
        }

        void exp_add(const unsigned& bitwidth, std::vector<unsigned>& lines, const std::vector<unsigned>& lhs, const std::vector<unsigned>& rhs) override;
        void exp_subtract(const unsigned& bitwidth, std::vector<unsigned>& lines, const std::vector<unsigned>& lhs, const std::vector<unsigned>& rhs) override;

        void exp_exor(const unsigned& bitwidth, std::vector<unsigned>& lines, const std::vector<unsigned>& lhs, const std::vector<unsigned>& rhs) override;
    };
} // namespace syrec
